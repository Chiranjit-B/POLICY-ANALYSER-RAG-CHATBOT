"""CLI entrypoint for running RAG-Multi-Corpus benchmarks."""

import argparse
from rag_pipeline.utils.config import load_config
from rag_pipeline.utils.logging import get_logger

logger = get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG pipeline on benchmark dataset.")
    parser.add_argument("--config", default="configs/base.yaml", help="Path to base config.")
    parser.add_argument("--benchmark-dir", default="bechmark", help="Path to benchmark directory.")
    args = parser.parse_args()

    cfg = load_config(args.config)
    logger.info("Loaded base config: %s", cfg)
    logger.info("Benchmark directory: %s", args.benchmark_dir)
    # TODO: Wire EvaluationRunner from rag_pipeline.evaluation.runner


if __name__ == "__main__":
    main()
