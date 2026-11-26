"""Format-specific document loaders and loader factory."""

from rag_pipeline.ingestion.loaders.base import BaseLoader
from rag_pipeline.ingestion.loaders.docx import DocxLoader
from rag_pipeline.ingestion.loaders.html import HtmlLoader
from rag_pipeline.ingestion.loaders.md import MarkdownLoader
from rag_pipeline.ingestion.loaders.pdf import PdfLoader
from rag_pipeline.ingestion.loaders.pptx import PptxLoader

LOADER_REGISTRY: dict[str, type[BaseLoader]] = {
    "pdf": PdfLoader,
    "docx": DocxLoader,
    "pptx": PptxLoader,
    "html": HtmlLoader,
    "htm": HtmlLoader,
    "md": MarkdownLoader,
}


def get_loader(file_format: str) -> BaseLoader:
    """Return an instantiated loader for the given file extension/format."""
    fmt = file_format.lower().lstrip(".")
    loader_cls = LOADER_REGISTRY.get(fmt)
    if loader_cls is None:
        raise ValueError(f"Unsupported document format: {file_format}")
    return loader_cls()


__all__ = [
    "BaseLoader",
    "PdfLoader",
    "DocxLoader",
    "PptxLoader",
    "HtmlLoader",
    "MarkdownLoader",
    "LOADER_REGISTRY",
    "get_loader",
]
