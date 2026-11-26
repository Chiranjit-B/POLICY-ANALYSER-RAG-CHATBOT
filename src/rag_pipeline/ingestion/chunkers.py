"""Structure-aware Markdown document chunking with contextual enrichment."""

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from rag_pipeline.utils.schemas import Chunk, Document

DEFAULT_HEADERS_TO_SPLIT_ON: list[tuple[str, str]] = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]


def _format_context_prefix(doc: Document, section_path: str) -> str:
    """Build a compact metadata header injected into chunk content for retrieval."""
    parts: list[str] = []
    if doc.domain:
        parts.append(f"Domain: {doc.domain}")
    parts.append(f"Document: {doc.doc_id}")
    if section_path:
        parts.append(f"Section: {section_path}")
    return f"[{' | '.join(parts)}]\n\n"


def chunk_document(
    doc: Document,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
    headers_to_split_on: list[tuple[str, str]] | None = None,
    strip_headers: bool = False,
    contextual_enrichment: bool = True,
) -> list[Chunk]:
    """Split a Markdown Document using two-stage structure-aware splitting.

    Stage 1: Split along Markdown heading boundaries (#, ##, ###) to preserve
    logical sections and attach header hierarchy to metadata.
    Stage 2: Recursively split oversized sections using paragraph/sentence
    separators while maintaining overlap, then optionally inject a metadata
    context prefix into each chunk's content.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")
    if not doc.content.strip():
        return []

    active_headers = headers_to_split_on or DEFAULT_HEADERS_TO_SPLIT_ON
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=active_headers,
        strip_headers=strip_headers,
    )
    section_docs = header_splitter.split_text(doc.content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    split_docs = text_splitter.split_documents(section_docs)

    chunks: list[Chunk] = []
    for idx, lc_doc in enumerate(split_docs):
        section_headers = [
            lc_doc.metadata[key]
            for _, key in active_headers
            if key in lc_doc.metadata
        ]
        section_path = " > ".join(section_headers)
        content = lc_doc.page_content
        if contextual_enrichment:
            content = _format_context_prefix(doc, section_path) + content

        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}::{doc.file_format}::chunk_{idx}",
                doc_id=doc.doc_id,
                content=content,
                chunk_index=idx,
                metadata={
                    "domain": doc.domain,
                    "file_format": doc.file_format,
                    "source_path": doc.source_path,
                    "section_path": section_path,
                    "contextual_enrichment": contextual_enrichment,
                    **doc.metadata,
                    **lc_doc.metadata,
                },
            )
        )
    return chunks
