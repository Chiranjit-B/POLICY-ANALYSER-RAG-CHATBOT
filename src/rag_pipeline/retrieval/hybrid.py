"""Hybrid retrieval combining dense and sparse results via Reciprocal Rank Fusion."""

from rag_pipeline.utils.schemas import RetrievedContext


def reciprocal_rank_fusion(
    result_lists: list[list[RetrievedContext]],
    k: int = 60,
    top_k: int = 10,
) -> list[RetrievedContext]:
    """Fuse multiple ranked context lists using Reciprocal Rank Fusion (RRF)."""
    scores: dict[str, float] = {}
    chunks_by_id: dict[str, RetrievedContext] = {}

    for results in result_lists:
        for rank, item in enumerate(results, start=1):
            cid = item.chunk.chunk_id
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
            if cid not in chunks_by_id:
                chunks_by_id[cid] = item

    sorted_ids = sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]
    return [
        chunks_by_id[cid].model_copy(
            update={"score": scores[cid], "retriever_type": "hybrid"}
        )
        for cid in sorted_ids
    ]
