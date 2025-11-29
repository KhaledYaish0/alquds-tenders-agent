from dataclasses import dataclass

from .keywords import (
    TENDER_KEYWORDS,
    ENGINEERING_KEYWORDS,
    SUPPLY_KEYWORDS,
    CONTRACTOR_KEYWORDS,
    JERUSALEM_KEYWORDS,
)


@dataclass
class PageClassification:
    page_number: int
    has_tender: bool
    is_engineering: bool
    is_supply_only: bool
    is_contractor_only: bool
    is_in_jerusalem: bool
    note: str


def _contains_any(text: str, keywords: list[str]) -> bool:
    """Return True if any of the given keywords appears in the text."""
    normalized = (text or "").lower()
    return any(kw.lower() in normalized for kw in keywords)


def classify_page(page_number: int, text: str) -> PageClassification:
    """
    Basic classification for an entire page.

    Later this can be extended to detect and extract each tender separately.
    """
    if not text:
        return PageClassification(
            page_number=page_number,
            has_tender=False,
            is_engineering=False,
            is_supply_only=False,
            is_contractor_only=False,
            is_in_jerusalem=False,
            note="Page has no text (might require OCR in the future).",
        )

    # Does this page look like it contains any tender / bid at all?
    has_tender = _contains_any(text, TENDER_KEYWORDS)

    if not has_tender:
        return PageClassification(
            page_number=page_number,
            has_tender=False,
            is_engineering=False,
            is_supply_only=False,
            is_contractor_only=False,
            is_in_jerusalem=False,
            note="No words found that indicate a tender / bid.",
        )

    # Determine which types of keywords are present
    has_engineering = _contains_any(text, ENGINEERING_KEYWORDS)
    has_supply = _contains_any(text, SUPPLY_KEYWORDS)
    has_contractor = _contains_any(text, CONTRACTOR_KEYWORDS)
    in_jerusalem = _contains_any(text, JERUSALEM_KEYWORDS)

    # Default flags
    is_engineering = False
    is_supply_only = False
    is_contractor_only = False
    note = ""

    # Khaled's rule:
    #   Any "pure supply" tender is not relevant to the office,
    #   even if engineering terms appear. The branches below
    #   encode this preference.

    # 1) Engineering-related keywords present → most important signal
    if has_engineering:
        is_engineering = True
        if has_supply or has_contractor:
            note = (
                "Page contains an engineering / consultancy tender relevant to the office; "
                "there may also be supply / execution tenders on the same page that can be ignored."
            )
        else:
            note = (
                "Engineering / consultancy tender (design, studies or preparation of tender "
                "documents) relevant to the office."
            )

    # 2) No engineering, only supply
    elif has_supply and not has_contractor:
        is_supply_only = True
        note = "Supply / delivery tender only (not relevant to the consultancy office)."

    # 3) No engineering, only contractor / execution
    elif has_contractor and not has_supply:
        is_contractor_only = True
        note = "Execution / contractor tender only (not relevant to the consultancy office)."

    # 4) Tender exists but type is unclear
    else:
        note = "Tender / bid announcement found, but its type is not clearly identified."

    if in_jerusalem:
        note += " (Related to Jerusalem and may be excluded later due to access difficulty.)"

    return PageClassification(
        page_number=page_number,
        has_tender=True,
        is_engineering=is_engineering,
        is_supply_only=is_supply_only,
        is_contractor_only=is_contractor_only,
        is_in_jerusalem=in_jerusalem,
        note=note,
    )
