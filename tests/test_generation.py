"""Tests for context builder and prompt formatting."""

from rag_pipeline.generation.context_builder import build_context_text
from rag_pipeline.utils.schemas import Chunk, RetrievedContext


def test_build_context_text_deduplicates_chunks() -> None:
    chunk = Chunk(
        chunk_id="c1",
        doc_id="d1",
        content="Sample fact.",
        chunk_index=0,
        metadata={"source_path": "datasets/a.md"},
    )
    contexts = [
        RetrievedContext(chunk=chunk, score=0.9),
        RetrievedContext(chunk=chunk, score=0.8),
    ]
    text = build_context_text(contexts)
    assert text.count("[c1]") == 1
