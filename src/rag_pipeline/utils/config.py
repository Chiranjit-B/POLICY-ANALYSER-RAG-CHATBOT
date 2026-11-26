"""Configuration loader for YAML pipeline configs and .env variables."""

from pathlib import Path
from typing import Any
import yaml
from dotenv import load_dotenv

load_dotenv()


def load_config(config_path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file into a dictionary."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
