"""CLI entrypoint for querying the RAG pipeline."""

import argparse
from rag_pipeline.utils.config import load_config
from rag_pipeline.utils.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the RAG pipeline.")
    parser.add_argument("--question", required=True, help="Question to ask.")
    parser.add_argument("--config", default="configs/retrieval.yaml", help="Path to retrieval config.")
    args = parser.parse_args()

    cfg = load_config(args.config)
    logger.info("Loaded retrieval config: %s", cfg)
    logger.info("Question: %s", args.question)
    # TODO: Wire retriever + generator from rag_pipeline.retrieval and rag_pipeline.generation


if __name__ == "__main__":
    main()
