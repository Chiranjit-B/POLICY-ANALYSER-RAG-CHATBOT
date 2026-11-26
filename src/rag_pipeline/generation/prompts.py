"""System and user prompt templates for grounded RAG generation."""

SYSTEM_PROMPT = (
    "You are a precise enterprise assistant. Answer the user's question using ONLY "
    "the provided context. Cite sources using [chunk_id]. If the answer is not in "
    "the context, state that you do not have enough information."
)


def build_user_prompt(question: str, context_text: str) -> str:
    """Format the user prompt with retrieved context."""
    return f"Context:\n{context_text}\n\nQuestion: {question}\n\nAnswer:"
