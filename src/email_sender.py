import resend
from typing import Optional
import os

def send_email_via_resend(subject: str, body: str, to_email: str) -> bool:
    """
    Send an email using Resend API.
    Returns True on success, False on failure.
    """
    resend.api_key = os.getenv("RESEND_API_KEY")


    try:
        result = resend.Emails.send({
            "from": "Tender Agent <onboarding@resend.dev>",
            "to": ["archplanningexperts@gmail.com"],
            "subject": subject,
            "html": body.replace("\n", "<br>"),
        })
        print(f"[EMAIL] Successfully sent! Message ID: {result['id']}")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email: {e}")
        return False
