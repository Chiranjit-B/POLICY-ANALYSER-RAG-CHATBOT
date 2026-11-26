"""PDF document loader using langchain-pymupdf4llm."""

from pathlib import Path
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from rag_pipeline.ingestion.loaders.base import BaseLoader
from rag_pipeline.utils.schemas import Document


class PdfLoader(BaseLoader):
    """Converts PDF files to Markdown using PyMuPDF4LLMLoader."""

    def load(self, file_path: Path, domain: str = "") -> Document:
        """Load a PDF file and return a Markdown-formatted Document."""
        loader = PyMuPDF4LLMLoader(str(file_path))
        pages = loader.load()
        content = "\n\n".join(page.page_content for page in pages if page.page_content)

        return Document(
            doc_id=file_path.stem,
            content=content,
            source_path=str(file_path),
            domain=domain,
            file_format="pdf",
            metadata={"page_count": len(pages)},
        )
