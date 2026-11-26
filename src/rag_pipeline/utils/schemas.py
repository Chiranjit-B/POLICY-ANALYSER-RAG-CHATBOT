"""Shared Pydantic schemas for documents, chunks, retrieval, and generation."""

from typing import Any
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Represents a parsed source document."""

    doc_id: str
    content: str
    source_path: str
    domain: str = ""
    file_format: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    """Represents a chunked segment of a document."""

    chunk_id: str
    doc_id: str
    content: str
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedContext(BaseModel):
    """Represents a retrieved chunk with relevance score."""

    chunk: Chunk
    score: float
    retriever_type: str = "hybrid"


class GeneratedAnswer(BaseModel):
    """Represents the final RAG answer with grounding citations."""

    question: str
    answer: str
    contexts: list[RetrievedContext] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
