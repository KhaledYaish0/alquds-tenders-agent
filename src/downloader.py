from pathlib import Path
from datetime import datetime
import re
import requests

ISSUES_DIR = Path("data/issues")
ALQUDS_PDF_PAGE_URL = "https://www.alquds.com/ar/issues"


def build_issue_filename(date: datetime) -> Path:
    """Builds a filename like: Al-Quds 25-11-2025.pdf"""
    fname = f"Al-Quds {date.day:02d}-{date.month:02d}-{date.year}.pdf"
    return ISSUES_DIR / fname


def fetch_latest_pdf_url_from_page() -> str | None:
    """Fetch the HTML page and extract the first PDF link."""
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


def download_issue_for_today() -> Path | None:
    """Downloads today's issue if available."""
    today = datetime.today()
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)

    local_path = build_issue_filename(today)

    if local_path.exists():
        print(f"Today's issue already exists: {local_path}")
        return local_path

    pdf_url = fetch_latest_pdf_url_from_page()
    if pdf_url is None:
        print("Could not determine today's PDF link.")
        return None

    print(f"Downloading today's issue from: {pdf_url}")

    try:
        resp = requests.get(pdf_url, timeout=60)
        content_type = resp.headers.get("content-type", "").lower()

        if resp.status_code == 200 and content_type.startswith("application/pdf"):
            with open(local_path, "wb") as f:
                f.write(resp.content)
            print(f"Saved today's issue to: {local_path}")
            return local_path

        else:
            print(
                f"Download failed. HTTP {resp.status_code}, "
                f"content-type={content_type}"
            )
            return None

    except Exception as e:
        print(f"Error during download: {e}")
        return None
