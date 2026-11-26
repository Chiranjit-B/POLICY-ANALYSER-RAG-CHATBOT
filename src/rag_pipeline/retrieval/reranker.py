"""Cross-encoder or LLM-based reranker."""

from rag_pipeline.utils.schemas import RetrievedContext


class Reranker:
    """Reranks retrieved contexts to improve precision at top-n."""

    def rerank(
        self, query: str, contexts: list[RetrievedContext], top_n: int = 5
    ) -> list[RetrievedContext]:
        """Return the top_n reranked contexts."""
        return sorted(contexts, key=lambda c: c.score, reverse=True)[:top_n]
