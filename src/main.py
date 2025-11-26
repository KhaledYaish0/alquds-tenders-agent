from pathlib import Path
import re

from .pdf_reader import extract_pages_text
from .tender_classifier import classify_page
from .report_builder import build_daily_report
from .downloader import download_issue_for_today  # 👈 مهم جداً


def analyze_issue(pdf_path: Path):
  
    m = re.search(r"(\d{2}-\d{2}-\d{4})", pdf_path.name)
    issue_date = m.group(1) if m else "تاريخ غير معروف"

    print(f" تحليل العدد: {pdf_path.name} (التاريخ: {issue_date})")
    pages = extract_pages_text(pdf_path)

    engineering_pages = []
    other_tender_pages = []

    for page in pages:
        page_no = page["page_number"]
        text = page["text"]

        cls = classify_page(page_no, text)

        if not cls.has_tender:
            continue

      
        print("-" * 60)
        print(f"صفحة {cls.page_number}")
        print(f"  ملاحظة: {cls.note}")
        print(f"  هندسي؟ {cls.is_engineering}")
        print(f"  توريد فقط؟ {cls.is_supply_only}")
        print(f"  مقاولات فقط؟ {cls.is_contractor_only}")
        print(f"  في القدس؟ {cls.is_in_jerusalem}")

        if cls.is_engineering:
            engineering_pages.append(cls)
        else:
            other_tender_pages.append(cls)

    print("\n ملخص العدد:")
    print(f"- عدد الصفحات ذات العطاءات الهندسية: {len(engineering_pages)}")
    print(f"- عدد الصفحات ذات عطاءات أخرى (توريد/مقاولات): {len(other_tender_pages)}")

    return issue_date, engineering_pages, other_tender_pages


if __name__ == "__main__":
  
    issue_path = download_issue_for_today()

    if issue_path is None:
        print(" لم يتم العثور على عدد اليوم (لا محليًا ولا عبر التنزيل).")
        raise SystemExit(1)

    # نحلل العدد
    issue_date, eng_pages, other_pages = analyze_issue(issue_path)

    # نبني تقرير الإيميل + الواتساب
    email_subject, email_body, whatsapp_msg = build_daily_report(
        issue_date=issue_date,
        engineering_pages=eng_pages,
    )

    print("\n" + "=" * 60)
    print(" اقتراح إيميل يمكن إرساله للوالد:\n")
    print("Subject:", email_subject)
    print()
    print(email_body)

    print("\n" + "=" * 60)
    print(" اقتراح رسالة واتساب:\n")
    print(whatsapp_msg)
