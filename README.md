# Al-Quds Tenders Agent 📰🤖

An automated Python tool that downloads the daily **Al-Quds** newspaper
issue (PDF), extracts pages that contain **tenders**, classifies them
(engineering / supply / contractor), and generates a ready-to-send
**email + WhatsApp summary** for an engineering office.

> 💬 **Arabic-first output**: All summaries and suggested messages are
> generated in Arabic, tailored for Palestinian engineering tenders.

------------------------------------------------------------------------

## 🚀 Main Features

-   📥 **Automatic issue download**
    -   Downloads today's Al-Quds issue as a PDF into `data/issues/`.
    -   Skips download if the file already exists locally.
-   📄 **PDF text extraction**
    -   Uses `pdfplumber` to extract text from each page.
    -   Handles pages with missing/invalid text gracefully.
-   🧠 **Tender classification per page** For each page the tool
    detects:
    -   Does this page contain a **tender / announcement / RFQ**?
    -   Is it an **engineering** tender?
    -   Is it **supply-only**?
    -   Is it **contractor-only**?
    -   Is it related to **Jerusalem** (القدس) or not?
-   📝 **Daily engineering tenders report**
    -   Counts engineering-related tender pages.
    -   Lists the detected pages with brief notes.
    -   Builds a clean Arabic **email body** to send to the office.
    -   Builds a short **WhatsApp message** for quick sharing.
-   ⚙️ **GitHub Actions automation**
    -   Optional workflow to run the script on a daily schedule using
        GitHub Actions.

------------------------------------------------------------------------

## 🗂 Project Structure

``` text
.
├── .github/
│   └── workflows/
│       └── alquds_daily.yml      # Optional CI job to run the script daily
├── data/
│   ├── issues/                   # Downloaded Al-Quds PDF issues (ignored in git)
│   └── annotated/ (optional)     # Manual analysis / annotation files (local only)
├── src/
│   ├── __init__.py
│   ├── main.py                   # Entry point: ties everything together
│   ├── downloader.py             # Download today's issue
│   ├── pdf_reader.py             # Read PDF pages & extract text
│   ├── keywords.py               # Arabic/English keyword lists
│   ├── tender_classifier.py      # Page-level classification logic
│   └── report_builder.py         # Email & WhatsApp message generator
├── read_pdf_pages.py             # Legacy / experimental script (optional)
├── requirements.txt
└── .gitignore
```

> 📝 **Note:**\
> `read_pdf_pages.py` is an older standalone script used during
> development.\
> The production-ready flow lives under `src/`.

------------------------------------------------------------------------

## 🧰 Tech Stack

-   **Language:** Python 3.10+
-   **PDF Processing:** `pdfplumber`
-   **HTTP Requests:** `requests`
-   **Automation:** GitHub Actions (optional)

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔧 Installation & Setup

``` bash
git clone https://github.com/KhaledYaish0/alquds-tenders-agent.git
cd alquds-tenders-agent

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

Ensure the data directory exists:

``` bash
mkdir -p data/issues
```

------------------------------------------------------------------------

## ▶️ Usage

### Run the project:

``` bash
python -m src.main
```

Process:

1.  Downloads today's issue (or uses existing local file).
2.  Extracts all PDF pages.
3.  Classifies each page (engineering / supply / contractor).
4.  Prints:
    -   Page-by-page tender summary
    -   Engineering-only summary
    -   Suggested Arabic **email**
    -   Suggested **WhatsApp message**

Output example:

``` text
✅ ملف عدد اليوم موجود مسبقاً: data/issues/Al-Quds 26-11-2025.pdf
📄 تحليل العدد: Al-Quds 26-11-2025.pdf (التاريخ: 26-11-2025)

صفحة 10:
  ملاحظة: عطاء توريد/تجهيز فقط
  هندسي؟ False
  توريد فقط؟ True
  مقاولات فقط؟ False
  في القدس؟ False

...

✉️ اقتراح إيميل يمكن إرساله للوالد:
(نص الإيميل...)

📲 اقتراح رسالة واتساب:
(نص الواتساب...)
```

------------------------------------------------------------------------

## ⚙️ Customization

Modify detection keywords via:

    src/keywords.py

Edit classification logic:

    src/tender_classifier.py

Change summary formatting:

    src/report_builder.py

------------------------------------------------------------------------

## 🤖 GitHub Actions (Optional)

Located at:

    .github/workflows/alquds_daily.yml

It can:

-   Run daily (cron)
-   Install dependencies
-   Execute:

``` bash
python -m src.main
```

Enable it in GitHub → Actions.

------------------------------------------------------------------------

## 🧪 Testing (Suggested)

Create folder:

    tests/

Example test:

``` python
def test_classify():
    from src.tender_classifier import classify_page
    cls = classify_page(1, "طرح عطاء إعداد التصاميم الهندسية")
    assert cls.is_engineering == True
```

Run:

``` bash
pytest
```

------------------------------------------------------------------------

## 🧠 Motivation

This tool automates the daily manual process of scanning the Al-Quds
newspaper to find engineering tenders relevant to Palestinian
engineering offices.

It saves time, prevents missed tenders, and provides ready-to-send
communication.

------------------------------------------------------------------------

## 📩 Contact

Created by **Khaled Yaish**\
Computer Engineer -- Palestine

For improvements or suggestions, open an issue or fork the repo.
