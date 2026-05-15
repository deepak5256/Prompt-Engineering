# Retrieval-Augmented Generation (RAG)

**Topic:** Advanced Patterns  
**Technique:** RAG — grounding LLM responses in a retrieved knowledge base  
**Institution:** Chanakya University — School of Engineering  
**Instructor:** Mr. Deepak B  
**Source:** [Lewis et al. 2020 — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"](https://arxiv.org/abs/2005.11401)  

---

## 1. The Problem RAG Solves

### The Hallucination Problem

Large language models are trained on a static snapshot of internet data. After training, they cannot learn new information. When asked about topics outside their training data, they **hallucinate** — generating plausible-sounding but factually wrong answers.

```
User: "What were Chanakya University's admissions criteria for 2026?"
LLM (no RAG): "Chanakya University typically requires a minimum of 60% in
               graduation..." [Completely fabricated — the model doesn't know]

LLM (with RAG): "According to the 2026 admissions document: Candidates must
                 have scored a minimum of 55% in their BCA/B.Sc. degree and
                 qualify the CUET entrance examination." [From actual document]
```

RAG fixes this by giving the model **real-time access to your documents** at query time.

---

## 2. RAG Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG SYSTEM ARCHITECTURE                   │
│                                                             │
│  OFFLINE (Indexing Pipeline)                               │
│  ┌────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  Documents │───▶│   Chunking   │───▶│  Embedding    │  │
│  │  (PDF/TXT) │    │  (split text)│    │  Model        │  │
│  └────────────┘    └──────────────┘    └───────┬───────┘  │
│                                                 │           │
│                                                 ▼           │
│                                        ┌─────────────────┐ │
│                                        │   Vector Store  │ │
│                                        │   (ChromaDB)    │ │
│                                        └────────┬────────┘ │
│                                                 │           │
│  ONLINE (Query Pipeline)                        │           │
│  ┌────────────┐    ┌──────────────┐             │           │
│  │  User      │───▶│   Embed      │             │           │
│  │  Query     │    │   Query      │             │           │
│  └────────────┘    └──────┬───────┘             │           │
│                           │                     │           │
│                           ▼     similarity       │           │
│                    ┌──────────────┐  search      │           │
│                    │  Retriever   │◀─────────────┘           │
│                    └──────┬───────┘                          │
│                           │ top-K chunks                     │
│                           ▼                                  │
│                    ┌──────────────┐                          │
│                    │   Augmented  │                          │
│                    │   Prompt     │                          │
│                    │  (context +  │                          │
│                    │   question)  │                          │
│                    └──────┬───────┘                          │
│                           │                                  │
│                           ▼                                  │
│                    ┌──────────────┐    ┌──────────────────┐ │
│                    │    LLM       │───▶│   Grounded       │ │
│                    │  (Gemini)    │    │   Answer         │ │
│                    └──────────────┘    └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. The Five RAG Pipeline Stages

### Stage 1: Document Ingestion

Loading your source documents into the pipeline.

**Supported formats:** PDF, DOCX, TXT, Markdown, HTML, CSV

```python
# Example: Loading a PDF
from pypdf import PdfReader

def load_pdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
```

### Stage 2: Text Chunking

Breaking documents into smaller, semantically coherent pieces. This is critical — chunks that are too large give the LLM irrelevant context; chunks that are too small lose meaning.

**Chunking strategies:**

| Strategy | Method | Best For |
|----------|--------|---------|
| **Fixed-size** | N characters, K overlap | Simple, fast, reliable |
| **Recursive** | Split on `\n\n`, `\n`, ` ` | General text |
| **Semantic** | Split at sentence/paragraph boundaries | Narrative text |
| **Structural** | Split by HTML/Markdown sections | Structured docs |

**Recommended default:** 500–800 tokens with 100–150 token overlap

```python
def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
```

### Stage 3: Embedding Generation

Converting text chunks into dense vector representations that capture semantic meaning.

```python
from sentence_transformers import SentenceTransformer

# Load embedding model (runs locally, free)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed chunks
def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embeddings = embed_model.encode(chunks, show_progress_bar=True)
    return embeddings.tolist()
```

**The embedding intuition:** Text with similar meaning produces vectors that are mathematically close to each other. "How do I reset my password?" and "Password recovery steps" will have very similar vector representations.

### Stage 4: Vector Storage and Retrieval

Storing embeddings in a vector database that supports fast similarity search.

```python
import chromadb

# Initialize persistent ChromaDB
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}  # Cosine similarity
)

# Store chunks with their embeddings
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# Retrieve top-K relevant chunks for a query
def retrieve(query: str, k: int = 5) -> list[str]:
    query_embedding = embed_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    return results["documents"][0]
```

### Stage 5: Augmented Generation

Constructing a prompt that includes retrieved context, then generating a grounded answer.

```python
def build_rag_prompt(query: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    
    return f"""You are a knowledgeable assistant. Answer the user's question using 
ONLY the information provided in the context below. 

If the answer is not found in the context, respond with: 
"I don't have information about that in the provided documents."

Do NOT use any knowledge outside the provided context.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""
```

---

## 4. RAG vs Fine-Tuning

This is one of the most common architectural decisions in AI system design.

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Knowledge update** | Instant (add documents) | Requires retraining |
| **Cost** | Low (retrieval + inference) | High (GPU training) |
| **Accuracy on domain** | High with good retrieval | Very high |
| **Hallucination risk** | Low (grounded in docs) | Medium (memorized) |
| **Data requirements** | Any documents | 1000s of examples |
| **Transparency** | Can cite sources | Black box |
| **Best for** | Dynamic, specific knowledge | Fixed style/behavior |

**For most production use cases, RAG is the right choice** unless you need to fundamentally change the model's behavior or style.

---

## 5. Advanced RAG Techniques

### Hybrid Search (Dense + Sparse)

Combine semantic search (embedding similarity) with keyword search (BM25) for better retrieval:

```
Score = α × dense_score + (1-α) × sparse_score
```

This handles cases where the user uses exact technical terms that embedding models might not capture well.

### Re-Ranking

After retrieving top-K chunks, use a cross-encoder to re-score and re-order them:

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, chunks: list[str], top_n: int = 3) -> list[str]:
    pairs = [[query, chunk] for chunk in chunks]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, chunks), reverse=True)
    return [chunk for _, chunk in ranked[:top_n]]
```

### Metadata Filtering

Add metadata to chunks (source, date, section) for filtered retrieval:

```python
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    metadatas=[{"source": "syllabus_2026.pdf", "page": i//5} for i in range(len(chunks))]
)

# Filter: only search within a specific document
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
    where={"source": "syllabus_2026.pdf"}
)
```

---

## 6. Evaluation: How to Know if Your RAG Works

### The RAGAS Framework

RAGAS (RAG Assessment) provides four key metrics:

| Metric | Measures | Ideal Value |
|--------|----------|-------------|
| **Faithfulness** | Is the answer supported by the retrieved context? | 1.0 |
| **Answer Relevancy** | Does the answer actually address the question? | 1.0 |
| **Context Precision** | Were the retrieved chunks relevant? | 1.0 |
| **Context Recall** | Did retrieval capture all needed information? | 1.0 |

A production RAG system should score >0.85 on all four metrics on your domain-specific test set.

---

## 7. Common RAG Failures and Fixes

| Failure | Symptom | Root Cause | Fix |
|---------|---------|-----------|-----|
| **Lost in the middle** | Model ignores chunks in middle of context | Attention degradation | Put most relevant chunks first/last |
| **Chunk too large** | Model answers partially | Irrelevant content in chunk dilutes signal | Reduce chunk size |
| **Chunk too small** | Context lacks coherence | Sentences lack surrounding context | Increase chunk size + overlap |
| **Wrong retrieval** | Model gets irrelevant chunks | Weak embeddings or query mismatch | Better embedding model or query rewriting |
| **Ignoring context** | Model uses training knowledge anyway | Weak system prompt | Add explicit instruction: "Use ONLY the provided context" |

---

## See the Working Implementation

The reference RAG system is in [`rag_system/`](./rag_system/). It implements all five stages above with a web interface, running entirely on your local machine.

---

*Previous: [Meta-Prompting ←](./03_meta_prompting.md)*  
*Next: [RAG System Code →](./rag_system/README.md)*  
*Back to [Topic 3 README](./README.md)*
