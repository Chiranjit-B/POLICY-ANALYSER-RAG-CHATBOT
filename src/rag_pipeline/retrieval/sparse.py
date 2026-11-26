"""Sparse keyword / BM25 retriever."""

from rag_pipeline.utils.schemas import RetrievedContext


class SparseRetriever:
    """Retrieves top-k chunks using lexical/BM25 matching."""

    def retrieve(self, query: str, top_k: int = 10) -> list[RetrievedContext]:
        """Search BM25 index for keyword-matching chunks."""
        raise NotImplementedError("Connect your BM25 index here.")
