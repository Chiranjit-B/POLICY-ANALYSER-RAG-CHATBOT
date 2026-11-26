"""Tests for structure-aware Markdown chunkers and contextual enrichment."""

from rag_pipeline.ingestion.chunkers import chunk_document
from rag_pipeline.utils.schemas import Document


def test_structure_chunking_preserves_headers_and_injects_context() -> None:
    content = (
        "# Account Policies\n\n"
        "## Wire Limits\n\n"
        + ("Daily wire limit is $50,000 for verified accounts. " * 6)
        + "\n\n## Fee Schedule\n\n"
        "Standard transfers are free."
    )
    doc = Document(
        doc_id="policies",
        content=content,
        source_path="datasets/ZX Bank/pdf/policies.pdf",
        domain="ZX Bank",
        file_format="pdf",
    )

    chunks = chunk_document(
        doc, chunk_size=150, chunk_overlap=20, contextual_enrichment=True
    )
    assert len(chunks) >= 3
    assert chunks[0].chunk_id.startswith("policies::pdf::chunk_")
    assert chunks[0].metadata["h1"] == "Account Policies"
    assert chunks[0].metadata["h2"] == "Wire Limits"
    assert chunks[0].metadata["section_path"] == "Account Policies > Wire Limits"
    assert chunks[1].content.startswith(
        "[Domain: ZX Bank | Document: policies | Section: Account Policies > Wire Limits]"
    )
    assert chunks[-1].metadata["h2"] == "Fee Schedule"


def test_chunk_document_without_contextual_enrichment() -> None:
    doc = Document(
        doc_id="notes",
        content="# Intro\n\nShort body.",
        source_path="datasets/CloudWay-24/pdf/notes.pdf",
        domain="CloudWay-24",
        file_format="pdf",
    )
    chunks = chunk_document(doc, contextual_enrichment=False)
    assert len(chunks) == 1
    assert not chunks[0].content.startswith("[Domain:")
