from pathlib import Path
import pdfplumber

def extract_pages_text(pdf_path: Path):
    """
    يرجّع list من:
    {
      'page_number': int,
      'text': str
    }
    """
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            pages_data.append({
                "page_number": i,
                "text": text,
            })

    return pages_data
