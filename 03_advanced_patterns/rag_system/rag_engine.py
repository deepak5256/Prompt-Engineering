"""
rag_engine.py — Core RAG Pipeline
Course: Prompt Engineering | Chanakya University — School of Engineering
Instructor: Mr. Deepak B

This module implements the full RAG pipeline:
  1. Document chunking
  2. Embedding generation (sentence-transformers, local)
  3. Vector store management (ChromaDB, local)
  4. Retrieval (cosine similarity search)
  5. Augmented generation (Google Gemini)
"""

import logging
from pathlib import Path
from typing import Optional

import chromadb
import google.generativeai as genai
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

import config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── RAG Engine ──────────────────────────────────────────────────────────────

class RAGEngine:
    """
    The complete Retrieval-Augmented Generation pipeline.

    Usage:
        engine = RAGEngine()
        engine.ingest_text("Your document content here", source="my_doc.txt")
        answer = engine.query("What is RAG?")
    """

    def __init__(self):
        logger.info("Initializing RAG Engine...")

        # 1. Validate API key
        if not config.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Get a free key at https://aistudio.google.com"
            )

        # 2. Configure Gemini
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.llm = genai.GenerativeModel(config.GEMINI_MODEL)
        logger.info(f"LLM: {config.GEMINI_MODEL}")

        # 3. Load embedding model (downloads ~80MB on first run)
        logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL} ...")
        self.embed_model = SentenceTransformer(config.EMBEDDING_MODEL)
        logger.info("Embedding model loaded.")

        # 4. Initialize ChromaDB (persistent local storage)
        Path(config.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(
            path=config.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(
            f"ChromaDB initialized. Collection '{config.COLLECTION_NAME}' "
            f"has {self.collection.count()} chunks."
        )

    # ─── Ingestion ────────────────────────────────────────────────────────────

    def chunk_text(self, text: str) -> list[str]:
        """
        Split text into overlapping fixed-size chunks.
        This is the 'Recursive Character' strategy with fixed chunk size.
        """
        chunks = []
        text = text.strip()
        start = 0

        while start < len(text):
            end = start + config.CHUNK_SIZE
            chunk = text[start:end].strip()
            if chunk:  # Skip empty chunks
                chunks.append(chunk)
            start += config.CHUNK_SIZE - config.CHUNK_OVERLAP

        return chunks

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of text strings."""
        embeddings = self.embed_model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return embeddings.tolist()

    def ingest_text(self, text: str, source: str = "unknown") -> dict:
        """
        Full ingestion pipeline: text → chunks → embeddings → ChromaDB.

        Args:
            text: Raw document text
            source: Source filename or identifier (for metadata)

        Returns:
            dict with chunks_added count
        """
        logger.info(f"Ingesting document: '{source}' ({len(text)} characters)")

        # Step 1: Chunk
        chunks = self.chunk_text(text)
        logger.info(f"  → {len(chunks)} chunks created (size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})")

        if not chunks:
            return {"chunks_added": 0, "source": source}

        # Step 2: Embed
        embeddings = self.embed_texts(chunks)

        # Step 3: Store in ChromaDB with unique IDs and metadata
        existing_count = self.collection.count()
        ids = [f"{source}_chunk_{existing_count + i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        logger.info(f"  → Stored in ChromaDB. Total chunks in DB: {self.collection.count()}")
        return {"chunks_added": len(chunks), "source": source}

    # ─── Retrieval ────────────────────────────────────────────────────────────

    def retrieve(self, query: str, k: int = None) -> list[dict]:
        """
        Embed query and retrieve top-K most similar chunks from ChromaDB.

        Returns:
            List of dicts: {text, source, distance}
        """
        k = k or config.TOP_K_RESULTS

        if self.collection.count() == 0:
            logger.warning("Vector store is empty. Please ingest documents first.")
            return []

        query_embedding = self.embed_texts([query])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved.append({
                "text": doc,
                "source": meta.get("source", "unknown"),
                "distance": round(dist, 4),
                "relevance_score": round(1 - dist, 4)  # Convert distance to similarity
            })

        return retrieved

    # ─── Generation ───────────────────────────────────────────────────────────

    def build_prompt(self, query: str, context_chunks: list[dict]) -> str:
        """
        Build the augmented prompt that grounds the LLM in retrieved context.
        This is the key prompt engineering step in RAG.
        """
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            context_parts.append(
                f"[Source {i}: {chunk['source']}]\n{chunk['text']}"
            )
        context_text = "\n\n" + "─" * 60 + "\n\n".join(context_parts)

        return f"""You are a precise and helpful assistant. Answer the user's question using ONLY the information provided in the context sections below.

CRITICAL RULES:
1. Base your answer exclusively on the provided context. Do not use external knowledge.
2. If the answer is not in the context, respond with exactly: "I don't have information about that in the provided documents."
3. Cite the source number (e.g., "[Source 1]") when using information from a specific chunk.
4. Be concise and direct. Do not add filler phrases.

CONTEXT:
{context_text}

QUESTION: {query}

ANSWER:"""

    def query(self, question: str) -> dict:
        """
        Full RAG query pipeline: question → retrieve → augment → generate.

        Args:
            question: The user's natural language question

        Returns:
            dict with answer, sources, and retrieved chunks
        """
        logger.info(f"Processing query: '{question}'")

        # Step 1: Retrieve relevant chunks
        chunks = self.retrieve(question)

        if not chunks:
            return {
                "answer": "The knowledge base is empty. Please ingest some documents first using the 'Ingest Documents' button.",
                "sources": [],
                "retrieved_chunks": []
            }

        # Step 2: Build augmented prompt
        prompt = self.build_prompt(question, chunks)

        # Step 3: Generate answer with Gemini
        response = self.llm.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=config.TEMPERATURE,
                max_output_tokens=config.MAX_OUTPUT_TOKENS,
            )
        )

        answer = response.text.strip()

        # Step 4: Return structured result
        sources = list(dict.fromkeys(c["source"] for c in chunks))  # Deduplicated

        logger.info(f"Answer generated. Sources used: {sources}")

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": [
                {
                    "text": c["text"][:200] + "..." if len(c["text"]) > 200 else c["text"],
                    "source": c["source"],
                    "relevance_score": c["relevance_score"]
                }
                for c in chunks
            ]
        }

    # ─── Status ───────────────────────────────────────────────────────────────

    def get_status(self) -> dict:
        """Return the current state of the vector store."""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "embedding_model": config.EMBEDDING_MODEL,
            "llm_model": config.GEMINI_MODEL,
            "collection_name": config.COLLECTION_NAME,
            "ready": count > 0
        }

    def reset(self) -> dict:
        """Clear all documents from the vector store."""
        self.chroma_client.delete_collection(config.COLLECTION_NAME)
        self.collection = self.chroma_client.get_or_create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Vector store cleared.")
        return {"message": "Knowledge base cleared successfully."}
