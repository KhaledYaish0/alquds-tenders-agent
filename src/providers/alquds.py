from __future__ import annotations

import re
import requests

ALQUDS_PDF_PAGE_URL = "https://www.alquds.com/ar/issues"


def fetch_latest_alquds_pdf_url() -> str | None:
    """Fetch the HTML page and extract the first PDF link for Al-Quds."""
    print(f"Fetching issue page from {ALQUDS_PDF_PAGE_URL}")

    try:
        resp = requests.get(ALQUDS_PDF_PAGE_URL, timeout=60)
    except Exception as e:
        print(f"Failed to fetch the page, network error: {e}")
        return None

    if resp.status_code != 200:
        print(f"Failed to fetch the page. HTTP {resp.status_code}")
        return None

    html = resp.text

    pattern = r"https://alquds\.fra1\.digitaloceanspaces\.com/uploads/[a-zA-Z0-9]+\.pdf"
    matches = re.findall(pattern, html)

    if not matches:
        print("No PDF link found in the page.")
        return None

    pdf_url = matches[0]
    print(f"Found PDF link: {pdf_url}")
    return pdf_url
