"""Abstract base class for document loaders."""

from abc import ABC, abstractmethod
from pathlib import Path
from rag_pipeline.utils.schemas import Document


class BaseLoader(ABC):
    """Interface that all format-specific loaders must implement."""

    @abstractmethod
    def load(self, file_path: Path, domain: str = "") -> Document:
        """Parse a file into a normalized Document object."""
