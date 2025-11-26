from typing import Sequence
from .tender_classifier import PageClassification

def build_daily_report(issue_date: str, engineering_pages: Sequence[PageClassification]):
    """
    يبني:
    - عنوان الإيميل
    - نص الإيميل
    - رسالة واتساب قصيرة
    """

    has_any = len(engineering_pages) > 0

    # عنوان الإيميل
    subject = f"تقرير العطاءات الهندسية – جريدة القدس – {issue_date}"

    if not has_any:
        # حالة: فش عطاءات هندسية
        body = (
            f"السلام عليكم أبو خالد،\n\n"
            f"تم فحص عدد جريدة القدس بتاريخ {issue_date}،\n"
            f"ولم يتم العثور على أي عطاءات هندسية أو استشارية مناسبة للمكتب.\n\n"
            f"تحياتي،\n"
            f"نظام متابعة العطاءات "
        )

        whatsapp = (
            f" تقرير عطاءات جريدة القدس – {issue_date}:\n"
            f"فش عطاءات هندسية اليوم."
        )
        return subject, body, whatsapp

    # في عطاءات هندسية
    # نبني جدول بسيط في الإيميل
    lines = []
    lines.append(f"السلام عليكم أبو خالد،\n")
    lines.append(f"تم فحص عدد جريدة القدس بتاريخ {issue_date}،")
    lines.append(f"وتم العثور على العطاءات/الإعلانات الهندسية التالية:\n")

    for cls in engineering_pages:
        line = f"- صفحة {cls.page_number}: {cls.note}"
        lines.append(line)

    lines.append("\nملاحظة: هذه النتائج أوتوماتيكية وقد تحتاج مراجعة سريعة من حضرتك.")
    lines.append("\nتحياتي،")
    lines.append("نظام متابعة العطاءات (كود خالد) ")

    email_body = "\n".join(lines)

    # رسالة واتساب مختصرة
    whatsapp_lines = []
    whatsapp_lines.append(f" تقرير عطاءات جريدة القدس – {issue_date}")
    whatsapp_lines.append(f"عدد الصفحات اللي فيها عطاءات هندسية: {len(engineering_pages)}")

    for cls in engineering_pages:
        whatsapp_lines.append(f"- صفحة {cls.page_number}: {cls.note}")

    whatsapp_msg = "\n".join(whatsapp_lines)

    return subject, email_body, whatsapp_msg
