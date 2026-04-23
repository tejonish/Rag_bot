from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

def generate_pdf_report(result_text, mode="candidate", filename="report.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    # Title
    title = "AI Hiring Copilot Report" if mode == "candidate" else "HR Evaluation Report"
    content.append(Paragraph(title, styles["Title"]))
    content.append(Spacer(1, 20))

    # Render line by line (NO parsing)
    for line in result_text.split("\n"):

        line = line.strip()

        if not line:
            content.append(Spacer(1, 10))
            continue

        # Headings
        if line.startswith(("🎯", "📄", "📊", "📚", "🔍")):
            content.append(Paragraph(f"<b>{line}</b>", styles["Heading2"]))

        # Section titles
        elif line.startswith(("✅", "⚠️", "❌")):
            content.append(Paragraph(f"<b>{line}</b>", styles["Heading3"]))

        # Bullet points
        elif line.startswith("-"):
            content.append(Paragraph(f"• {line[1:].strip()}", styles["Normal"]))

        else:
            content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)

    return filename

