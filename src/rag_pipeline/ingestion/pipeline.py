"""Folder-wise ingestion pipeline: load -> clean -> save .md -> structure-split -> save chunks."""

from pathlib import Path
from typing import Any
from rag_pipeline.ingestion.chunkers import chunk_document
from rag_pipeline.ingestion.cleaners import clean_document
from rag_pipeline.ingestion.loaders import get_loader
from rag_pipeline.utils.logging import get_logger
from rag_pipeline.utils.schemas import Chunk, Document

logger = get_logger(__name__)


def _parse_headers_config(
    raw_headers: list[list[str]] | None,
) -> list[tuple[str, str]] | None:
    if not raw_headers:
        return None
    return [(pair[0], pair[1]) for pair in raw_headers]


def ingest_domain_folder(
    domain_dir: Path,
    parsed_dir: Path,
    chunks_dir: Path,
    config: dict[str, Any],
    skip_existing: bool = False,
) -> list[Chunk]:
    """Process all supported format folders inside a single domain directory."""
    domain = domain_dir.name
    supported_formats: list[str] = config.get(
        "supported_formats", ["pdf", "md", "html", "docx", "pptx"]
    )
    chunk_cfg: dict[str, Any] = config.get("chunking", {})
    chunk_size = int(chunk_cfg.get("chunk_size", 800))
    chunk_overlap = int(chunk_cfg.get("chunk_overlap", 100))
    strip_headers = bool(chunk_cfg.get("strip_headers", False))
    contextual_enrichment = bool(chunk_cfg.get("contextual_enrichment", True))
    headers_to_split_on = _parse_headers_config(chunk_cfg.get("headers_to_split_on"))

    domain_chunks: list[Chunk] = []

    for fmt in supported_formats:
        fmt_dir = domain_dir / fmt
        if not fmt_dir.is_dir():
            continue

        loader = get_loader(fmt)
        out_fmt_dir = parsed_dir / domain / fmt
        out_fmt_dir.mkdir(parents=True, exist_ok=True)

        for file_path in sorted(fmt_dir.iterdir()):
            if not file_path.is_file() or file_path.name.startswith("."):
                continue
            if file_path.stat().st_size == 0 or file_path.suffix.lower().lstrip(".") != fmt:
                logger.debug("Skipping empty or mismatched file: %s", file_path)
                continue

            parsed_md_path = out_fmt_dir / f"{file_path.stem}.md"
            if skip_existing and parsed_md_path.exists():
                doc = Document(
                    doc_id=file_path.stem,
                    content=parsed_md_path.read_text(encoding="utf-8"),
                    source_path=str(file_path),
                    domain=domain,
                    file_format=fmt,
                    metadata={"parsed_path": str(parsed_md_path)},
                )
            else:
                try:
                    raw_doc = loader.load(file_path, domain=domain)
                except Exception as exc:
                    logger.warning("Failed to load %s: %s", file_path, exc)
                    continue

                doc = clean_document(raw_doc)
                doc = doc.model_copy(
                    update={"metadata": {**doc.metadata, "parsed_path": str(parsed_md_path)}}
                )
                parsed_md_path.write_text(doc.content, encoding="utf-8")

            chunks = chunk_document(
                doc,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                headers_to_split_on=headers_to_split_on,
                strip_headers=strip_headers,
                contextual_enrichment=contextual_enrichment,
            )
            domain_chunks.extend(chunks)

    chunks_dir.mkdir(parents=True, exist_ok=True)
    chunks_out = chunks_dir / f"{domain}.jsonl"
    with chunks_out.open("w", encoding="utf-8") as f:
        for chunk in domain_chunks:
            f.write(chunk.model_dump_json() + "\n")

    logger.info(
        "Domain '%s': wrote %d chunks to %s", domain, len(domain_chunks), chunks_out
    )
    return domain_chunks


def run_ingestion_pipeline(
    datasets_dir: str | Path,
    parsed_dir: str | Path,
    chunks_dir: str | Path,
    config: dict[str, Any],
    domain_filter: str | None = None,
    skip_existing: bool = False,
) -> dict[str, int]:
    """Run folder-wise ingestion across all domain directories in datasets_dir."""
    datasets_path = Path(datasets_dir)
    parsed_path = Path(parsed_dir)
    chunks_path = Path(chunks_dir)

    if not datasets_path.is_dir():
        raise FileNotFoundError(f"Datasets directory not found: {datasets_path}")

    summary: dict[str, int] = {}
    for entry in sorted(datasets_path.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if domain_filter and entry.name != domain_filter:
            continue

        chunks = ingest_domain_folder(
            domain_dir=entry,
            parsed_dir=parsed_path,
            chunks_dir=chunks_path,
            config=config,
            skip_existing=skip_existing,
        )
        summary[entry.name] = len(chunks)

    return summary
