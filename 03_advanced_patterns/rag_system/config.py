"""
config.py — Configuration for the RAG System
Course: Prompt Engineering | Chanakya University — School of Engineering
Instructor: Mr. Deepak B
"""

import os

# ─── API Configuration ────────────────────────────────────────────────────────
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL: str = "gemini-1.5-flash"       # Free tier; change to gemini-1.5-pro for higher quality

# ─── Embedding Configuration ─────────────────────────────────────────────────
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"    # 384-dim, runs locally, ~80MB download
EMBEDDING_DIMENSION: int = 384

# ─── Chunking Configuration ───────────────────────────────────────────────────
CHUNK_SIZE: int = 600          # Characters per chunk
CHUNK_OVERLAP: int = 100       # Overlap between adjacent chunks

# ─── Retrieval Configuration ─────────────────────────────────────────────────
TOP_K_RESULTS: int = 5         # Number of chunks to retrieve per query
SIMILARITY_THRESHOLD: float = 0.0   # Minimum cosine similarity (0 = no filter)

# ─── Vector Store Configuration ──────────────────────────────────────────────
CHROMA_PERSIST_DIR: str = "./chroma_store"
COLLECTION_NAME: str = "rag_knowledge_base"

# ─── LLM Generation Configuration ────────────────────────────────────────────
MAX_OUTPUT_TOKENS: int = 1024
TEMPERATURE: float = 0.1       # Low temperature for factual, grounded answers

# ─── Sample Documents Directory ──────────────────────────────────────────────
SAMPLE_DOCS_DIR: str = "./sample_docs"

# ─── Server Configuration ─────────────────────────────────────────────────────
HOST: str = "0.0.0.0"
PORT: int = 8000
