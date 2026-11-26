"""Batch embedding and vector/BM25 index upsert."""

from rag_pipeline.utils.schemas import Chunk


class Indexer:
    """Indexes Document chunks into vector and/or sparse stores."""

    def __init__(self, vector_store_dir: str = "data/vector_store") -> None:
        self.vector_store_dir = vector_store_dir

    def index_chunks(self, chunks: list[Chunk]) -> int:
        """Embed and store chunks. Returns number of indexed chunks."""
        raise NotImplementedError("Connect your embedding model and vector store here.")
