"""
app.py — FastAPI Application Entry Point
Course: Prompt Engineering | Chanakya University — School of Engineering
Instructor: Mr. Deepak B

API Endpoints:
  GET  /              → Serve the frontend UI
  GET  /status        → Vector store status (chunk count, models, ready flag)
  POST /ingest        → Load all sample documents into the vector store
  POST /ingest/text   → Ingest raw text string
  POST /query         → Ask a question; returns answer + sources + chunks
  POST /reset         → Clear the vector store
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import config
from ingest import load_sample_documents
from rag_engine import RAGEngine

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Pydantic Request/Response Models ────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000, description="The question to answer")

class TextIngestRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Raw text to add to the knowledge base")
    source: str = Field(default="manual_input", description="Source identifier")

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    retrieved_chunks: list[dict]

class IngestResponse(BaseModel):
    message: str
    documents_processed: int
    total_chunks_added: int

# ─── App Initialization ───────────────────────────────────────────────────────

# Lazy initialization — engine created on first request to avoid startup delays
_engine: RAGEngine | None = None

def get_engine() -> RAGEngine:
    """Get or create the RAG engine (singleton)."""
    global _engine
    if _engine is None:
        _engine = RAGEngine()
    return _engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG engine on startup."""
    logger.info("=" * 60)
    logger.info("  RAG System — Chanakya University School of Engineering")
    logger.info("  Instructor: Mr. Deepak B | Prompt Engineering Course")
    logger.info("=" * 60)
    try:
        get_engine()  # Pre-load the engine
        logger.info("RAG Engine ready.")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Engine: {e}")
        logger.error("Make sure GEMINI_API_KEY is set correctly.")
    yield
    logger.info("Shutting down RAG System.")

# ─── FastAPI App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="RAG System — Prompt Engineering Course",
    description="Retrieval-Augmented Generation reference implementation for Chanakya University",
    version="1.0.0",
    lifespan=lifespan
)

# CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the browser frontend."""
    frontend_path = Path(__file__).parent / "frontend" / "index.html"
    if not frontend_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(str(frontend_path))


@app.get("/status")
async def get_status():
    """
    Check the status of the RAG system.
    Returns chunk count, model names, and whether the system is ready.
    """
    try:
        engine = get_engine()
        return engine.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse)
async def ingest_sample_documents():
    """
    Load all sample documents from the sample_docs/ directory into ChromaDB.
    This is the main ingestion endpoint used by the UI.
    """
    try:
        engine = get_engine()
        documents = load_sample_documents()

        if not documents:
            raise HTTPException(
                status_code=404,
                detail=f"No documents found in '{config.SAMPLE_DOCS_DIR}'. Add .txt or .pdf files there."
            )

        total_chunks = 0
        for text, source in documents:
            result = engine.ingest_text(text, source=source)
            total_chunks += result["chunks_added"]

        return IngestResponse(
            message=f"Successfully ingested {len(documents)} document(s).",
            documents_processed=len(documents),
            total_chunks_added=total_chunks
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during ingestion")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/text", response_model=IngestResponse)
async def ingest_text(request: TextIngestRequest):
    """
    Add raw text directly to the knowledge base.
    Useful for pasting text without creating a file.
    """
    try:
        engine = get_engine()
        result = engine.ingest_text(request.text, source=request.source)
        return IngestResponse(
            message=f"Text ingested as '{request.source}'.",
            documents_processed=1,
            total_chunks_added=result["chunks_added"]
        )
    except Exception as e:
        logger.exception("Error ingesting text")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Answer a question using the RAG pipeline.

    Pipeline:
      1. Embed the question
      2. Retrieve top-K similar chunks from ChromaDB
      3. Build augmented prompt (context + question)
      4. Generate grounded answer with Gemini
      5. Return answer + source citations
    """
    try:
        engine = get_engine()
        result = engine.query(request.question)
        return QueryResponse(**result)
    except Exception as e:
        logger.exception("Error processing query")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_knowledge_base():
    """Clear all documents from the vector store."""
    try:
        engine = get_engine()
        return engine.reset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Starting RAG System on http://{config.HOST}:{config.PORT}")
    print(f"  API Docs:   http://localhost:{config.PORT}/docs")
    print(f"{'='*60}\n")

    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,       # Auto-reload on code changes during development
        log_level="info"
    )
