from pathlib import Path
from datetime import datetime
import requests

from .providers.alquds import fetch_latest_alquds_pdf_url
from .providers.alayam import fetch_latest_alayam_pdf_url

ISSUES_DIR = Path("data/issues")


def build_issue_filename(source: str, date: datetime) -> Path:
    """Builds a filename like: Al-Quds 25-11-2025.pdf or Al-Ayyam 25-11-2025.pdf"""
    fname = f"{source} {date.day:02d}-{date.month:02d}-{date.year}.pdf"
    return ISSUES_DIR / fname


def _download_single_issue(source: str, pdf_url: str | None, date: datetime) -> Path | None:
    """Helper function to download one PDF if url is available."""
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)

    if pdf_url is None:
        print(f"[{source}] Could not determine today's PDF link.")
        return None

    local_path = build_issue_filename(source, date)

    if local_path.exists():
        print(f"[{source}] Today's issue already exists: {local_path}")
        return local_path

    print(f"[{source}] Downloading today's issue from: {pdf_url}")

    try:
        resp = requests.get(pdf_url, timeout=60)
        content_type = resp.headers.get("content-type", "").lower()

        if resp.status_code == 200 and content_type.startswith("application/pdf"):
            with open(local_path, "wb") as f:
                f.write(resp.content)
            print(f"[{source}] Saved today's issue to: {local_path}")
            return local_path
        else:
            print(
                f"[{source}] Download failed. HTTP {resp.status_code}, "
                f"content-type={content_type}"
            )
            return None

    except Exception as e:
        print(f"[{source}] Error during download: {e}")
        return None


def download_issues_for_today() -> list[Path]:
    """Downloads today's issues from all providers and returns paths for the ones that succeeded."""
    today = datetime.today()
    issues: list[Path] = []

    # Al-Quds
    alquds_url = fetch_latest_alquds_pdf_url()
    alquds_path = _download_single_issue("Al-Quds", alquds_url, today)
    if alquds_path is not None:
        issues.append(alquds_path)

    # Al-Ayyam
    alayam_url = fetch_latest_alayam_pdf_url()
    alayam_path = _download_single_issue("Al-Ayyam", alayam_url, today)
    if alayam_path is not None:
        issues.append(alayam_path)

    return issues
