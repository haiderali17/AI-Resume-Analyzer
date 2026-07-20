import json
from services.groq_service import GroqService
from utils.file_handler import FileHandler
from utils.pdf_generator import PDFGenerator


class ResumeService:
    def __init__(self):
        self.file_handler = FileHandler()
        self.groq = GroqService()
        self.pdf = PDFGenerator()

    def analyze_resume(
        self,
        file_path: str,
        output_path: str
    ):

        resume_text = self.file_handler.read_file(file_path)

        analysis = self.groq.analyze_resume(resume_text)

        self.file_handler.save_report(
            output_path,
            json.dumps(analysis, indent=4)
        )

        # Generate PDF Report
        self.pdf.generate(
            analysis,
            "data/reports/resume_report.pdf"
        )

        return analysis