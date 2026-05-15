"""
ingest.py — Document Loading Utilities for the RAG System
Course: Prompt Engineering | Chanakya University — School of Engineering
Instructor: Mr. Deepak B

Handles loading text from:
  - Plain text files (.txt, .md)
  - PDF files (.pdf)
  - Direct string input (for API uploads)
"""

import logging
from pathlib import Path

from pypdf import PdfReader

import config

logger = logging.getLogger(__name__)


def load_text_file(filepath: str | Path) -> str:
    """Load a plain text or markdown file."""
    path = Path(filepath)
    try:
        text = path.read_text(encoding="utf-8")
        logger.info(f"Loaded text file: {path.name} ({len(text)} chars)")
        return text
    except Exception as e:
        logger.error(f"Failed to load {path}: {e}")
        raise


def load_pdf_file(filepath: str | Path) -> str:
    """
    Extract text from a PDF file page by page.
    Note: PDFs with scanned images (no text layer) will return empty strings.
    """
    path = Path(filepath)
    try:
        reader = PdfReader(str(path))
        pages_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages_text.append(f"[Page {i+1}]\n{page_text}")

        full_text = "\n\n".join(pages_text)
        logger.info(f"Loaded PDF: {path.name} ({len(reader.pages)} pages, {len(full_text)} chars)")
        return full_text
    except Exception as e:
        logger.error(f"Failed to load PDF {path}: {e}")
        raise


def load_document(filepath: str | Path) -> tuple[str, str]:
    """
    Load any supported document type.

    Returns:
        (text_content, source_name) tuple
    """
    path = Path(filepath)
    suffix = path.suffix.lower()

    if suffix in (".txt", ".md"):
        return load_text_file(path), path.name
    elif suffix == ".pdf":
        return load_pdf_file(path), path.name
    else:
        raise ValueError(
            f"Unsupported file type: '{suffix}'. Supported: .txt, .md, .pdf"
        )


def load_sample_documents() -> list[tuple[str, str]]:
    """
    Load all documents from the configured sample_docs directory.

    Returns:
        List of (text_content, source_name) tuples
    """
    docs_dir = Path(config.SAMPLE_DOCS_DIR)

    if not docs_dir.exists():
        logger.warning(f"Sample docs directory not found: {docs_dir}")
        return []

    documents = []
    supported_extensions = {".txt", ".md", ".pdf"}

    for filepath in sorted(docs_dir.iterdir()):
        if filepath.suffix.lower() in supported_extensions and filepath.is_file():
            try:
                text, source = load_document(filepath)
                if text.strip():
                    documents.append((text, source))
            except Exception as e:
                logger.error(f"Skipping {filepath.name}: {e}")

    logger.info(f"Loaded {len(documents)} documents from {docs_dir}")
    return documents
