"""Context packing, deduplication, and token-budget management."""

from rag_pipeline.utils.schemas import RetrievedContext


def build_context_text(contexts: list[RetrievedContext], max_chars: int = 12000) -> str:
    """Format retrieved chunks into a deduplicated context block within a character budget."""
    seen: set[str] = set()
    parts: list[str] = []
    total_chars = 0

    for item in contexts:
        cid = item.chunk.chunk_id
        if cid in seen:
            continue
        seen.add(cid)

        block = f"[{cid}] (source: {item.chunk.metadata.get('source_path', 'unknown')})\n{item.chunk.content}"
        if total_chars + len(block) > max_chars:
            break
        parts.append(block)
        total_chars += len(block)

    return "\n\n---\n\n".join(parts)
