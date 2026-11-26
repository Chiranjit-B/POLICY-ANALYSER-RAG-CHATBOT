"""Dense vector similarity retriever."""

from rag_pipeline.utils.schemas import RetrievedContext


class DenseRetriever:
    """Retrieves top-k chunks using dense vector embeddings."""

    def retrieve(self, query: str, top_k: int = 10) -> list[RetrievedContext]:
        """Search vector store for semantically similar chunks."""
        raise NotImplementedError("Connect your vector store client here.")
