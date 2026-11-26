"""API request and response schemas."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    domain: str | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: list[str] = Field(default_factory=list)
