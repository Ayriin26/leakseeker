from typing import List, Dict, Any
from collections import Counter
from datetime import datetime
from pathlib import Path
import base64
import io
import webbrowser
import html

from leakseeker.ai_helper import generate_ai_explanation

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


RISK_COLORS = {
    "critical": "#ef4444",
    "high":     "#f97316",
    "medium":   "#eab308",
    "low":      "#22c55e",
}


def generate_summary(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    counter = Counter(f.get("risk_level", "low") for f in findings)
    return {
        "total": len(findings),
        "critical": counter.get("critical", 0),
        "high": counter.get("high", 0),
        "medium": counter.get("medium", 0),
        "low": counter.get("low", 0),
    }


def calculate_risk_score(findings: List[Dict[str, Any]]) -> int:
    weights = {"critical": 10, "high": 7, "medium": 4, "low": 1}
    score = sum(weights.get(f.get("risk_level", "low"), 1) for f in findings)
    return min(score, 100)


def _chart_b64(summary: Dict[str, int]) -> str:
    if not MATPLOTLIB_AVAILABLE:
        return ""

    labels = ["Critical", "High", "Medium", "Low"]
    values = [summary["critical"], summary["high"], summary["medium"], summary["low"]]
    colors = ["#ef4444", "#f97316", "#eab308", "#22c55e"]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(labels, values, color=colors)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode('utf-8')


def _redact(text: str) -> str:
    text = str(text)
    if len(text) > 12:
        return text[:5] + '••••' + text[-4:]
    return text[:3] + '•••'


def generate_html_report(findings: List[Dict[str, Any]], output_file=None):
    downloads_path = Path.home() / "Downloads"
    downloads_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_file is None:
        output_file = downloads_path / f"LeakSeeker_Report_{timestamp}.html"
    else:
        output_file = Path(output_file)

    summary = generate_summary(findings)
    risk_score = calculate_risk_score(findings)

    # Sort by risk + confidence
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings_sorted = sorted(
        findings,
        key=lambda f: (
            order.get(f.get("risk_level", "low"), 4),
            -f.get("confidence", 0)
        )
    )

    chart_b64 = _chart_b64(summary)
    chart_img = f'<img src="data:image/png;base64,{chart_b64}" width="400"/>' if chart_b64 else ""

    rows = ""
    for f in findings_sorted:
        ai_text = generate_ai_explanation(f.get("secret_type"), f.get("matched_text", ""))

        rows += f"""
        <div class="card">
            <div class="header">
                <span class="badge" style="background:{RISK_COLORS.get(f['risk_level'], '#999')}">
                    {f['risk_level'].upper()}
                </span>
                <span class="confidence">{f.get('confidence', 'N/A')}%</span>
            </div>

            <div class="meta">
                <b>Type:</b> {html.escape(f.get('secret_type', ''))}<br>
                <b>Location:</b> {html.escape(f.get('file', ''))}:{f.get('line_number', '')}<br>
                <b>Match:</b> <code>{_redact(f.get('matched_text', ''))}</code>
            </div>

            <div class="ai">
                {html.escape(ai_text).replace('\\n', '<br>')}
            </div>
        </div>
        """

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>LeakSeeker Report</title>
<style>
body {{
    background:#0f172a;
    color:white;
    font-family: Arial;
    padding:20px;
}}

.card {{
    background:#1e293b;
    padding:15px;
    border-radius:10px;
    margin-bottom:15px;
}}

.header {{
    display:flex;
    justify-content:space-between;
    margin-bottom:10px;
}}

.badge {{
    padding:4px 8px;
    border-radius:5px;
    font-weight:bold;
}}

.confidence {{
    font-size:14px;
    color:#94a3b8;
}}

.meta {{
    font-size:14px;
    margin-bottom:10px;
}}

.ai {{
    font-size:13px;
    color:#cbd5f5;
    background:#0f172a;
    padding:10px;
    border-radius:6px;
}}
</style>
</head>
<body>

<h1>LeakSeeker Report</h1>
<p>Generated: {datetime.now()}</p>

<h2>Risk Score: {risk_score}/100</h2>
{chart_img}

<hr>

{rows}

</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"📄 Report saved: {output_file}")
    webbrowser.open(output_file.as_uri())