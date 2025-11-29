from pathlib import Path
import pdfplumber
from typing import List, Dict, Any


def extract_pages_text(pdf_path: Path) -> list[dict[str, str | int]]:
    """
    Extract text from all pages of a PDF.

    Returns a list of dictionaries of the form:
        {
            "page_number": int,
            "text": str
        }
    """
    pages_data: list[dict[str, str | int]] = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""

            pages_data.append(
                {
                    "page_number": i,
                    "text": text,
                }
            )

    return pages_data
