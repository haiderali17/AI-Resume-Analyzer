from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def generate(self, analysis, output_path):

        doc = SimpleDocTemplate(output_path)
        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"]))
        elements.append(Paragraph(f"<b>ATS Score:</b> {analysis['ats_score']}/100", styles["Normal"]))

        elements.append(Paragraph("<br/><b>Strengths</b>", styles["Heading2"]))
        for item in analysis["strengths"]:
            elements.append(Paragraph(f"• {item}", styles["Normal"]))

        elements.append(Paragraph("<br/><b>Weaknesses</b>", styles["Heading2"]))
        for item in analysis["weaknesses"]:
            elements.append(Paragraph(f"• {item}", styles["Normal"]))

        elements.append(Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"]))
        for item in analysis["missing_skills"]:
            elements.append(Paragraph(f"• {item}", styles["Normal"]))

        elements.append(Paragraph("<br/><b>Suggestions</b>", styles["Heading2"]))
        for item in analysis["suggestions"]:
            elements.append(Paragraph(f"• {item}", styles["Normal"]))

        doc.build(elements)