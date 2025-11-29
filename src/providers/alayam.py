from __future__ import annotations

import re
import requests

ALAYAM_PDF_PAGE_URL = "https://www.al-ayyam.ps/ar/PDF"
ALAYAM_BASE_URL = "https://www.al-ayyam.ps"


def fetch_latest_alayam_pdf_url() -> str | None:
    """Fetch the Al-Ayyam PDF page and extract the all.pdf link for today's full issue."""
    print(f"Fetching Al-Ayyam PDF page from {ALAYAM_PDF_PAGE_URL}")

    try:
        resp = requests.get(ALAYAM_PDF_PAGE_URL, timeout=60)
    except Exception as e:
        print(f"Failed to fetch Al-Ayyam page, network error: {e}")
        return None

    if resp.status_code != 200:
        print(f"Failed to fetch Al-Ayyam page. HTTP {resp.status_code}")
        return None

    html = resp.text

    # مثال: /public/pdfs/2025/11/29/all/all.pdf
    pattern = r"/public/pdfs/\d{4}/\d{2}/\d{2}/all/all\.pdf"
    match = re.search(pattern, html)

    if not match:
        print("No all.pdf link found for Al-Ayyam.")
        return None

    href = match.group(0)
    pdf_url = ALAYAM_BASE_URL + href
    print(f"Found Al-Ayyam all.pdf link: {pdf_url}")
    return pdf_url
