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

        # Read uploaded file
        resume_text = self.file_handler.read_file(file_path)

        # -----------------------------
        # STEP 1: Validate Resume
        # -----------------------------
        validation = self.groq.validate_resume(resume_text)

        if not validation.get("is_resume", False):
            raise ValueError(
                validation.get(
                    "reason",
                    "The uploaded document is not a valid Resume/CV."
                )
            )

        # -----------------------------
        # STEP 2: Analyze Resume
        # -----------------------------
        analysis = self.groq.analyze_resume(resume_text)

        # Save JSON Report
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