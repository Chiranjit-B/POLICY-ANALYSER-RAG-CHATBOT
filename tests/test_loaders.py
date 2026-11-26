"""Tests for document loaders and loader factory."""

from pathlib import Path
import pytest
from rag_pipeline.ingestion.loaders import (
    DocxLoader,
    HtmlLoader,
    MarkdownLoader,
    PdfLoader,
    PptxLoader,
    get_loader,
)


def test_markdown_loader(tmp_path: Path) -> None:
    md_file = tmp_path / "sample.md"
    md_file.write_text("# Title\n\nBody text.", encoding="utf-8")

    doc = MarkdownLoader().load(md_file, domain="test")
    assert doc.doc_id == "sample"
    assert doc.file_format == "md"
    assert doc.domain == "test"
    assert "Body text." in doc.content


def test_html_loader_converts_to_atx_markdown(tmp_path: Path) -> None:
    html_file = tmp_path / "page.html"
    html_file.write_text(
        "<html><head><title>Spec</title><style>body{}</style></head>"
        "<body><h1>Overview</h1><p>Fast <b>motor</b>.</p></body></html>",
        encoding="utf-8",
    )

    doc = HtmlLoader().load(html_file, domain="Aventro Motors")
    assert doc.file_format == "html"
    assert "# Overview" in doc.content
    assert "body{}" not in doc.content


def test_get_loader_factory() -> None:
    assert isinstance(get_loader("pdf"), PdfLoader)
    assert isinstance(get_loader("docx"), DocxLoader)
    assert isinstance(get_loader("pptx"), PptxLoader)
    assert isinstance(get_loader("html"), HtmlLoader)
    assert isinstance(get_loader("md"), MarkdownLoader)

    with pytest.raises(ValueError):
        get_loader("exe")
