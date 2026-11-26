"""Tests for retrieval and fusion logic."""

from rag_pipeline.retrieval.hybrid import reciprocal_rank_fusion
from rag_pipeline.utils.schemas import Chunk, RetrievedContext


def _make_ctx(chunk_id: str, score: float) -> RetrievedContext:
    return RetrievedContext(
        chunk=Chunk(chunk_id=chunk_id, doc_id="d1", content=chunk_id, chunk_index=0),
        score=score,
    )


def test_reciprocal_rank_fusion_ranks_overlap_highest() -> None:
    dense = [_make_ctx("c1", 0.9), _make_ctx("c2", 0.8)]
    sparse = [_make_ctx("c2", 5.0), _make_ctx("c3", 4.0)]

    fused = reciprocal_rank_fusion([dense, sparse], top_k=3)
    assert fused[0].chunk.chunk_id == "c2"
    assert fused[0].retriever_type == "hybrid"
