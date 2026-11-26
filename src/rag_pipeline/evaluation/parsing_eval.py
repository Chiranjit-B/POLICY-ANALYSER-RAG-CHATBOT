"""Document parsing accuracy and cross-format consistency metrics."""

from rag_pipeline.utils.schemas import Document


def compute_char_coverage(extracted: Document, reference_text: str) -> float:
    """Measure character-length ratio between extracted text and reference text."""
    if not reference_text:
        return 0.0
    return min(len(extracted.content) / len(reference_text), 1.0)
