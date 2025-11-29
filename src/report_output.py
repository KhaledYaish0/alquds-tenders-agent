from pathlib import Path
import webbrowser


def render_report_html(
    summary_text: str,
    email_body: str,
    report_filename: str,
) -> Path:
    """
    Render a simple HTML report that contains:
      - a text summary
      - the suggested email body

    Returns the absolute path to the HTML file.
    """
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / report_filename

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Tender Daily Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1 {{ margin-bottom: 0.5rem; }}
    pre {{
      background: #f5f5f5;
      padding: 1rem;
      border-radius: 4px;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <h1>Tender Daily Report</h1>

  <h2>Summary</h2>
  <pre>{summary_text}</pre>

  <h2>Suggested Email</h2>
  <pre>{email_body}</pre>
</body>
</html>
"""

    path.write_text(html, encoding="utf-8")
    return path.resolve()


def open_report_in_browser(path: Path) -> None:
    """Open the given HTML report in the default web browser."""
    abs_path = Path(path).resolve()
    print(f"Opening report in browser: {abs_path}")
    webbrowser.open(abs_path.as_uri())
