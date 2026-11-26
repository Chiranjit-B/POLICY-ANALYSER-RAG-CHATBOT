"""DOCX document loader using langchain-docling."""

from pathlib import Path
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from rag_pipeline.ingestion.loaders.base import BaseLoader
from rag_pipeline.utils.schemas import Document


class DocxLoader(BaseLoader):
    """Converts Word (.docx) files to Markdown using DoclingLoader."""

    def load(self, file_path: Path, domain: str = "") -> Document:
        """Load a DOCX file and export it as Markdown."""
        loader = DoclingLoader(
            file_path=str(file_path),
            export_type=ExportType.MARKDOWN,
        )
        docs = loader.load()
        content = "\n\n".join(d.page_content for d in docs if d.page_content)

        return Document(
            doc_id=file_path.stem,
            content=content,
            source_path=str(file_path),
            domain=domain,
            file_format="docx",
        )
