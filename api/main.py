"""FastAPI application exposing /health and /query endpoints."""

from fastapi import FastAPI
from api.schemas import QueryRequest, QueryResponse

app = FastAPI(title="RAG-Multi-Corpus API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    """Query the RAG pipeline (wire retriever + generator here)."""
    return QueryResponse(
        question=request.question,
        answer="RAG pipeline not yet connected.",
        citations=[],
    )
