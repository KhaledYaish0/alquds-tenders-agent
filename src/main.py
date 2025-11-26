from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

from .pdf_reader import extract_pages_text
from .tender_classifier import classify_page, PageClassification
from .report_builder import build_daily_report
from .downloader import download_issue_for_today


def analyze_issue(pdf_path: Path) -> None:
    """يحلّل عدد واحد من الجريدة ويطبع التقرير الكامل."""
    m = re.search(r"(\d{2}-\d{2}-\d{4})", pdf_path.name)
    issue_date = m.group(1) if m else "تاريخ غير معروف"

    print(f"تحليل العدد: {pdf_path.name} (التاريخ: {issue_date})")

    pages = extract_pages_text(pdf_path)

    classifications: list[PageClassification] = []

    for page in pages:
        page_num = page["page_number"]
        text = page["text"] or ""
        cls = classify_page(page_num, text)
        classifications.append(cls)

        
        if cls.has_tender:
            print("-" * 60)
            print(f"صفحة {cls.page_number}")
            print(f"  ملاحظة: {cls.note}")
            print(f"  هندسي؟ {cls.is_engineering}")
            print(f"  توريد فقط؟ {cls.is_supply_only}")
            print(f"  مقاولات فقط؟ {cls.is_contractor_only}")
            print(f"  في القدس؟ {cls.is_in_jerusalem}")

    eng_pages = [c for c in classifications if c.is_engineering]
    other_tenders = [
        c
        for c in classifications
        if c.has_tender and not c.is_engineering
    ]

    print("\n ملخص العدد:")
    print(f"- عدد الصفحات ذات العطاءات الهندسية: {len(eng_pages)}")
    print(f"- عدد الصفحات ذات عطاءات أخرى (توريد/مقاولات): {len(other_tenders)}")

    print("\n" + "=" * 60)

    subject, email_body, whatsapp_msg = build_daily_report(
        issue_date=issue_date,
        engineering_pages=eng_pages,
    )

    print(" اقتراح إيميل يمكن إرساله للوالد:\n")
    print(f"Subject: {subject}\n")
    print(email_body)
    print("\n" + "=" * 60)
    print(" اقتراح رسالة واتساب:\n")
    print(whatsapp_msg)
    print("\n")


def main() -> int:
    """
    نقطة الدخول الرئيسية.
    مهم: حتى لو فشل تنزيل الجريدة (403 من GitHub مثلاً)،
    ما بدنا نرجّع exit code 1 عشان الـ workflow ما يفشل.
    """
    pdf_path = download_issue_for_today()

    if pdf_path is None or not pdf_path.exists():
        print(
       "Could not retrieve today's issue (neither locally nor via download).\n"
        "   If you are running this inside GitHub Actions, the server most likely blocked\n"
        "   the request (HTTP 403). This is a known issue caused by Al-Quds blocking\n"
        "   cloud/CI IP ranges.\n"
        "   Please run the script locally or on a VPS for a successful download."
        )
        
        return 0

    analyze_issue(pdf_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
