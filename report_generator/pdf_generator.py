import markdown2
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
from weasyprint import HTML


def generate_pdf_report(md_path, pdf_path):
    styles = getSampleStyleSheet()
    story = []
    with open(md_path, 'r', encoding='utf-8') as f:
        html = markdown2.markdown(f.read())

    for line in html.split("\n"):
        story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 12))

    doc = SimpleDocTemplate(str(pdf_path), pagesize=LETTER)
    doc.build(story)


def generate_pdf_with_weasyprint(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        html_content = markdown2.markdown(f.read())
    HTML(string=html_content).write_pdf(str(pdf_path))
