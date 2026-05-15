# RAG System — Reference Implementation

**Course:** Prompt Engineering | Topic 3: Advanced Patterns  
**Institution:** Chanakya University — School of Engineering  
**Instructor:** Mr. Deepak B  
**Assignment:** Week 3 — Build a Working RAG System  

---

## What This System Does

This is a **fully working Retrieval-Augmented Generation (RAG) system** that:
- Accepts text documents as your knowledge base
- Splits, embeds, and stores them in a local ChromaDB vector database
- Lets you ask questions and get answers grounded in your documents
- Runs 100% locally — no cloud databases required
- Uses Google Gemini API for text generation (free tier available)

**Tech Stack:**
| Component | Technology | Why |
|-----------|-----------|-----|
| Web Framework | FastAPI | Industry-standard Python API framework |
| Vector Database | ChromaDB | Persistent, local, zero-config |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) | Free, runs offline, 384-dimensional |
| LLM | Google Gemini 1.5 Flash | Free tier, high quality |
| PDF Parsing | PyPDF | Lightweight, no dependencies |
| Frontend | Vanilla HTML/CSS/JS | No build tools needed |

---

## Setup & Run

### Prerequisites
- Python 3.10+
- A free Google Gemini API key from [aistudio.google.com](https://aistudio.google.com) → API Key

### Installation

```bash
# Navigate to the RAG system directory
cd 03_advanced_patterns/rag_system

# Create a virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set your API key (Windows)
set GEMINI_API_KEY=your_api_key_here

# Set your API key (Mac/Linux)
# export GEMINI_API_KEY=your_api_key_here

# Start the application
python app.py
```

### Using the System

1. Open **http://localhost:8000** in your browser
2. Click **"Ingest Documents"** — loads the sample documents from `sample_docs/`
3. Type a question in the chat box
4. The system retrieves relevant chunks and generates a grounded answer
5. See which source documents were used below the answer

---

## File Structure

```
rag_system/
├── README.md          ← This file
├── requirements.txt   ← Python dependencies
├── config.py          ← Configuration (API key, chunk size, etc.)
├── app.py             ← FastAPI application — the main entry point
├── rag_engine.py      ← Core RAG pipeline logic
├── ingest.py          ← Document loading and indexing
├── chroma_store/      ← ChromaDB database (auto-created on first run)
├── sample_docs/       ← Sample knowledge base documents
│   ├── prompt_engineering_basics.txt
│   ├── rag_concepts.txt
│   └── llm_overview.txt
└── frontend/
    └── index.html     ← Browser interface
```

---

## Architecture Diagram

```
Browser (index.html)
       │
       │  HTTP requests
       ▼
FastAPI (app.py)          ← Routes: POST /ingest, POST /query, GET /status
       │
       │  calls
       ▼
RAG Engine (rag_engine.py)
       │
       ├── Ingest path:
       │   Document → Chunks → Embeddings → ChromaDB
       │
       └── Query path:
           Query → Embed → ChromaDB similarity search → Top-K chunks
                → Build prompt → Gemini API → Answer
```

---

*See the code files for full implementation details.*
