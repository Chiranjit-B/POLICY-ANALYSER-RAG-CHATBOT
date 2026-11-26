"""Text cleaning, normalization, and boilerplate removal."""

import re
from rag_pipeline.utils.schemas import Document


def clean_text(text: str) -> str:
    """Normalize whitespace and strip excessive blank lines."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_document(doc: Document) -> Document:
    """Return a copy of the Document with cleaned content."""
    return doc.model_copy(update={"content": clean_text(doc.content)})
