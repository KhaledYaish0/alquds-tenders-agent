from pathlib import Path
from datetime import datetime
import re
import requests

ISSUES_DIR = Path("data/issues")

ALQUDS_PDF_PAGE_URL = "https://www.alquds.com/ar/issues"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def build_issue_filename(date: datetime) -> Path:
    """يبني اسم ملف PDF مثل: Al-Quds 25-11-2025.pdf"""
    fname = f"Al-Quds {date.day:02d}-{date.month:02d}-{date.year}.pdf"
    return ISSUES_DIR / fname


def fetch_latest_pdf_url_from_page() -> str | None:
    """
    يفتح صفحة الويب اللي فيها الجريدة، ويدور على أول رابط PDF
    من دومين alquds.fra1.digitaloceanspaces.com.
    """
    print(f"جلب صفحة الجريدة من الانترنت {ALQUDS_PDF_PAGE_URL}")
    try:
        
        resp = requests.get(ALQUDS_PDF_PAGE_URL, headers=HEADERS, timeout=60)
    except Exception as e:
        print(f"فشل في جلب الصفحة، خطأ شبكة: {e}")
        return None

    if resp.status_code != 200:
        print(f"فشل في جلب الصفحة HTTP: {resp.status_code}")
        return None

    html = resp.text

    pattern = r"https://alquds\.fra1\.digitaloceanspaces\.com/uploads/[a-zA-Z0-9]+\.pdf"
    matches = re.findall(pattern, html)

    if not matches:
        print(" لم يتم العثور على أي رابط PDF في الصفحة.")
        return None

    pdf_url = matches[0]
    print(f" تم العثور على رابط PDF: {pdf_url}")
    return pdf_url


def download_issue_for_today() -> Path | None:
    """
    يحاول تنزيل عدد اليوم:
    - إذا كان موجود مسبقاً في data/issues → يرجع المسار.
    - إذا مش موجود → يحاول جلب آخر PDF من صفحة الجريدة.
    """
    today = datetime.today()
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)

    local_path = build_issue_filename(today)
    if local_path.exists():
        print(f" ملف عدد اليوم موجود مسبقاً: {local_path}")
        return local_path

    pdf_url = fetch_latest_pdf_url_from_page()
    if pdf_url is None:
        print(" لم نتمكن من تحديد رابط PDF لعدد اليوم.")
        return None

    print(f" تنزيل عدد اليوم من: {pdf_url}")
    try:
        
        resp = requests.get(pdf_url, headers=HEADERS, timeout=60)
        content_type = resp.headers.get("content-type", "").lower()

        if resp.status_code == 200 and content_type.startswith("application/pdf"):
            with open(local_path, "wb") as f:
                f.write(resp.content)
            print(f" تم تنزيل عدد اليوم وحفظه في: {local_path}")
            return local_path
        else:
            print(
                f" فشل التنزيل، كود HTTP: {resp.status_code} "
                f"أو نوع محتوى غير PDF ({content_type})."
            )
            return None
    except Exception as e:
        print(f" حصل خطأ أثناء التنزيل: {e}")
        return None
