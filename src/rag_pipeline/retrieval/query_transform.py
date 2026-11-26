"""Query transformation: rewriting, HyDE, multi-query expansion, domain routing."""


def rewrite_query(query: str) -> str:
    """Normalize or rewrite a user query before retrieval."""
    return query.strip()
