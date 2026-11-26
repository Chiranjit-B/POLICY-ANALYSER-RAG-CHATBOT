"""LLM answer generator with citation support."""

from rag_pipeline.generation.context_builder import build_context_text
from rag_pipeline.generation.prompts import SYSTEM_PROMPT, build_user_prompt
from rag_pipeline.utils.schemas import GeneratedAnswer, RetrievedContext


class AnswerGenerator:
    """Generates grounded answers from retrieved contexts."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1) -> None:
        self.model = model
        self.temperature = temperature

    def generate(
        self, question: str, contexts: list[RetrievedContext]
    ) -> GeneratedAnswer:
        """Build prompt from contexts and call the configured LLM."""
        context_text = build_context_text(contexts)
        _ = SYSTEM_PROMPT
        _ = build_user_prompt(question, context_text)
        raise NotImplementedError("Connect your LLM client (OpenAI/Gemini/Anthropic) here.")
