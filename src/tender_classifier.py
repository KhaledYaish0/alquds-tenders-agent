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
    t = (text or "").lower()
    return any(kw.lower() in t for kw in keywords)


def classify_page(page_number: int, text: str) -> PageClassification:
    """
    تصنيف مبدئي للصفحة كاملة.
    لاحقاً ممكن نطوره ليسحب كل عطاء لحاله.
    """
    if not text:
        return PageClassification(
            page_number=page_number,
            has_tender=False,
            is_engineering=False,
            is_supply_only=False,
            is_contractor_only=False,
            is_in_jerusalem=False,
            note="صفحة بدون نص (قد تحتاج OCR لاحقاً).",
        )

    has_tender = _contains_any(text, TENDER_KEYWORDS)

    if not has_tender:
        return PageClassification(
            page_number=page_number,
            has_tender=False,
            is_engineering=False,
            is_supply_only=False,
            is_contractor_only=False,
            is_in_jerusalem=False,
            note="لا يوجد كلمات تدل على عطاء/مناقصة.",
        )

    # نحدد نوع الكلمات اللي ظهرت في النص
    has_engineering = _contains_any(text, ENGINEERING_KEYWORDS)
    has_supply = _contains_any(text, SUPPLY_KEYWORDS)
    has_contractor = _contains_any(text, CONTRACTOR_KEYWORDS)
    in_jerusalem = _contains_any(text, JERUSALEM_KEYWORDS)

    # القيم الافتراضية
    is_engineering = False
    is_supply_only = False
    is_contractor_only = False
    note = ""

    # 🔴 قاعدة خالد: أي توريد = مش شغل المكتب، حتى لو مذكور هندسي
        # القيم الافتراضية
    is_engineering = False
    is_supply_only = False
    is_contractor_only = False

    # 1) لو في إشارات هندسية → أهم إشارة
    if has_engineering:
        is_engineering = True
        if has_supply or has_contractor:
            note = "الصفحة تحتوي على عطاء استشاري/هندسي مناسب للمكتب، وقد توجد عطاءات توريد/تنفيذ أخرى في نفس الصفحة لا تهمنا."
        else:
            note = "عطاء استشاري / هندسي (تصميم أو دراسات أو إعداد وثائق عطاء) مناسب للمكتب."

    # 2) مافي هندسي، بس في توريد
    elif has_supply and not has_contractor:
        is_supply_only = True
        note = "عطاء توريد/تجهيز فقط (غير مهم للمكتب الاستشاري)."

    # 3) مافي هندسي، بس في مقاولات
    elif has_contractor and not has_supply:
        is_contractor_only = True
        note = "عطاء تنفيذ/مقاولات فقط (غير مناسب للمكتب الاستشاري)."

    # 4) نوع مش واضح
    else:
        note = "إعلان عطاء/مناقصة لكن نوعه غير واضح تماماً."
    if in_jerusalem:
        note += " (مرتبط بالقدس، وقد يستبعد لاحقاً لصعوبة الوصول)."

    return PageClassification(
        page_number=page_number,
        has_tender=True,
        is_engineering=is_engineering,
        is_supply_only=is_supply_only,
        is_contractor_only=is_contractor_only,
        is_in_jerusalem=in_jerusalem,
        note=note,
    )
