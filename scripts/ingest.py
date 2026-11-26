"""CLI entrypoint for folder-wise document ingestion and structure-based splitting."""

import argparse
from rag_pipeline.ingestion.pipeline import run_ingestion_pipeline
from rag_pipeline.utils.config import load_config
from rag_pipeline.utils.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert multi-format dataset folders to Markdown and split by structure."
    )
    parser.add_argument(
        "--config", default="configs/ingestion.yaml", help="Path to ingestion config."
    )
    parser.add_argument(
        "--datasets-dir", default="datasets", help="Path to raw datasets directory."
    )
    parser.add_argument(
        "--parsed-dir", default="data/parsed", help="Directory for converted .md files."
    )
    parser.add_argument(
        "--chunks-dir", default="data/chunks", help="Directory for output chunk JSONL files."
    )
    parser.add_argument(
        "--domain", default=None, help="Optional single domain folder name to ingest."
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Reuse existing converted .md files in data/parsed/ if present.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    summary = run_ingestion_pipeline(
        datasets_dir=args.datasets_dir,
        parsed_dir=args.parsed_dir,
        chunks_dir=args.chunks_dir,
        config=cfg,
        domain_filter=args.domain,
        skip_existing=args.skip_existing,
    )
    logger.info("Ingestion complete. Chunk counts by domain: %s", summary)


if __name__ == "__main__":
    main()
