"""HTML document loader using langchain-community and markdownify."""

from pathlib import Path
from bs4 import BeautifulSoup
from langchain_community.document_loaders import BSHTMLLoader
from markdownify import markdownify as html_to_markdown
from rag_pipeline.ingestion.loaders.base import BaseLoader
from rag_pipeline.utils.schemas import Document


class HtmlLoader(BaseLoader):
    """Converts HTML files to ATX-style Markdown using BSHTMLLoader + markdownify."""

    def load(self, file_path: Path, domain: str = "") -> Document:
        """Load an HTML file, strip non-content tags, and convert to Markdown."""
        raw_html = file_path.read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        markdown_content = html_to_markdown(
            str(soup),
            heading_style="ATX",
            bullets="-",
        )

        # Extract title via BSHTMLLoader metadata when available
        title = ""
        try:
            bs_docs = BSHTMLLoader(str(file_path)).load()
            if bs_docs:
                title = bs_docs[0].metadata.get("title", "") or ""
        except Exception:
            title = soup.title.string.strip() if soup.title and soup.title.string else ""

        return Document(
            doc_id=file_path.stem,
            content=markdown_content,
            source_path=str(file_path),
            domain=domain,
            file_format="html",
            metadata={"title": title} if title else {},
        )
