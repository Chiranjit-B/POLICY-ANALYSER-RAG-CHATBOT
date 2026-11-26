"""Markdown document loader."""

from pathlib import Path
from rag_pipeline.ingestion.loaders.base import BaseLoader
from rag_pipeline.utils.schemas import Document


class MarkdownLoader(BaseLoader):
    """Reads Markdown (.md) files into Document objects."""

    def load(self, file_path: Path, domain: str = "") -> Document:
        """Read a Markdown file into a Document."""
        content = file_path.read_text(encoding="utf-8")
        return Document(
            doc_id=file_path.stem,
            content=content,
            source_path=str(file_path),
            domain=domain,
            file_format="md",
        )
