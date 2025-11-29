from __future__ import annotations

from pathlib import Path
import re
from .email_sender import send_email_via_resend

from .report_output import render_report_html, open_report_in_browser
from .pdf_reader import extract_pages_text
from .tender_classifier import classify_page, PageClassification
from .report_builder import build_daily_report
from .downloader import download_issues_for_today


def analyze_issue(pdf_path: Path) -> None:
    """
    Analyze a single newspaper issue PDF and print a full summary/report.
    Also generates an HTML report and opens it in the browser.
    """
    # Extract date from filename, e.g. 'Al-Quds 29-11-2025.pdf'
    m = re.search(r"(\d{2}-\d{2}-\d{4})", pdf_path.name)
    issue_date = m.group(1) if m else "Unknown date"

    # Infer the source name from the filename prefix (e.g. 'Al-Quds', 'Al-Ayyam')
    source_name = pdf_path.name.split(" ", 1)[0]

    print(f"\n=== Analyzing issue: {pdf_path.name} ===")
    print(f"Source: {source_name} | Date: {issue_date}")

    pages = extract_pages_text(pdf_path)
    classifications: list[PageClassification] = []

    for page in pages:
        page_num = page["page_number"]
        text = page["text"] or ""
        cls = classify_page(page_num, text)
        classifications.append(cls)

        if cls.has_tender:
            print("-" * 60)
            print(f"Page {cls.page_number}")
            print(f"  Note: {cls.note}")
            print(f"  Engineering? {cls.is_engineering}")
            print(f"  Supply only? {cls.is_supply_only}")
            print(f"  Contractor only? {cls.is_contractor_only}")
            print(f"  In Jerusalem? {cls.is_in_jerusalem}")

    eng_pages = [c for c in classifications if c.is_engineering]
    other_tenders = [c for c in classifications if c.has_tender and not c.is_engineering]

    print("\nIssue summary:")
    print(f"- Number of pages with engineering tenders: {len(eng_pages)}")
    print(f"- Number of pages with other tenders (supply/contractor): {len(other_tenders)}")
    print("\n" + "=" * 60)

    subject, email_body, whatsapp_msg = build_daily_report(
        issue_date=issue_date,
        source_name=source_name,
        engineering_pages=eng_pages,
    )

    print("Suggested email to send to your father:\n")
    print(f"Subject: {subject}\n")
    print(email_body)
    print("\n" + "=" * 60)
    print("Suggested WhatsApp message:\n")
    print(whatsapp_msg)
    print("\n")

       
    send_email_success = send_email_via_resend(
        subject,
        email_body,
        "archplanningexperts@gmail.com", 
    )
    print(f"Email send status: {send_email_success}")


    # Short text summary for the HTML report
    summary_text = (
        f"Newspaper: {source_name}\n"
        f"Issue date: {issue_date}\n"
        f"Engineering tenders pages: {len(eng_pages)}\n"
        f"Other tenders pages: {len(other_tenders)}"
    )

    # Build a specific report filename per newspaper, e.g.:
    #   al-quds_report_29-11-2025.html
    #   al-ayyam_report_29-11-2025.html
    slug_source = source_name.lower().replace(" ", "-")
    report_filename = f"{slug_source}_report_{issue_date}.html"

    report_path = render_report_html(summary_text, email_body, report_filename)
    print(f"HTML report saved to: {report_path}")
    open_report_in_browser(report_path)


def main() -> int:
    """
    Application entry point.

    Note:
    Even if downloading the newspapers fails (for example due to HTTP 403
    when running inside GitHub Actions), we always return exit code 0 so
    that the workflow is not marked as failed.
    """
    print("=== Starting Daily Tender Agent ===")

    pdf_paths = download_issues_for_today()
    print(f"Download finished. Number of issues found: {len(pdf_paths)}")

    if not pdf_paths:
        print(
            "Could not retrieve today's issues (neither locally nor via download).\n"
            "If you are running this inside GitHub Actions, the server most likely "
            "blocked the request (HTTP 403). This is a known issue caused by "
            "Al-Quds / Al-Ayyam servers blocking cloud/CI IP ranges.\n"
            "Please run the script locally or on a VPS for a successful download."
        )
        return 0

    for pdf_path in pdf_paths:
        analyze_issue(pdf_path)

    print("=== Daily Tender Agent finished ===")
    return 0


if __name__ == "__main__":

    raise SystemExit(main())
