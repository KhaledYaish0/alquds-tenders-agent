import pdfplumber
from pathlib import Path


pdf_path = Path("data/issues/Al-Quds 26-11-2025.pdf")

with pdfplumber.open(pdf_path) as pdf:
    print(f"Page # {len(pdf.pages)}")

    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        print("=" * 40)
        print(f"Page {i}")
        print("-" * 40)
        # اطبع أول 500 حرف بس عشان ما يعبي الشاشة
        print(text[:500])
