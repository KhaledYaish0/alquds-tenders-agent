from typing import Sequence
from .tender_classifier import PageClassification


def build_daily_report(
    issue_date: str,
    source_name: str,
    engineering_pages: Sequence[PageClassification],
):
    """
    Build:
      - email subject
      - email body
      - short WhatsApp message
    for a single newspaper issue.
    """

    has_any = len(engineering_pages) > 0

    # Email subject (now includes the newspaper name)
    subject = f"Engineering tenders report – {source_name} – {issue_date}"

    if not has_any:
        # Case: no engineering tenders found
        body = (
            "Hello,\n\n"
            f"The {source_name} issue dated {issue_date} has been reviewed,\n"
            "and no suitable engineering / consultancy tenders were found.\n\n"
            "Best regards,\n"
            "Tender Monitoring System"
        )

        whatsapp = (
            f"Engineering tenders report – {source_name} – {issue_date}:\n"
            "No engineering tenders found today."
        )
        return subject, body, whatsapp

    # Case: at least one engineering tender
    lines: list[str] = []
    lines.append("Hello,\n")
    lines.append(f"The {source_name} issue dated {issue_date} has been reviewed,")
    lines.append(
        "and the following engineering / consultancy tenders were found:\n"
    )

    for cls in engineering_pages:
        line = f"- Page {cls.page_number}: {cls.note}"
        lines.append(line)

    lines.append(
        "\nNote: This result is generated automatically and may need a quick manual review."
    )
    lines.append("\nBest regards,")
    lines.append("Tender Monitoring System (Khaled's code)")

    email_body = "\n".join(lines)

    # Short WhatsApp message
    whatsapp_lines: list[str] = []
    whatsapp_lines.append(
        f"Engineering tenders report – {source_name} – {issue_date}"
    )
    whatsapp_lines.append(
        f"Number of pages with engineering tenders: {len(engineering_pages)}"
    )

    for cls in engineering_pages:
        whatsapp_lines.append(f"- Page {cls.page_number}: {cls.note}")

    whatsapp_msg = "\n".join(whatsapp_lines)

    return subject, email_body, whatsapp_msg
