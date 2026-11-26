"""Generation evaluation: faithfulness, answer correctness, hallucination rate."""

from rag_pipeline.utils.schemas import GeneratedAnswer


def evaluate_answer(generated: GeneratedAnswer, ground_truth: str) -> dict[str, float]:
    """Placeholder for LLM-as-a-judge or semantic similarity answer evaluation."""
    raise NotImplementedError("Implement answer evaluation metrics here.")
