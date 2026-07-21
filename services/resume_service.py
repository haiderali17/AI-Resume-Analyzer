import json
import re

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

        text = resume_text.lower()

        # ==================================================
        # FAST RULE-BASED GUARD
        # ==================================================

        resume_sections = [
            "summary",
            "objective",
            "education",
            "experience",
            "work experience",
            "employment",
            "skills",
            "technical skills",
            "projects",
            "certifications",
            "achievements",
            "languages",
            "internships",
            "references"
        ]

        blocked_keywords = [
            "offer letter",
            "internship offer",
            "appointment letter",
            "joining letter",
            "experience certificate",
            "certificate of completion",
            "internship certificate",
            "recommendation letter",
            "to whom it may concern",
            "research paper",
            "assignment",
            "invoice",
            "receipt",
            "bank statement",
            "dear sir",
            "dear madam",
            "congratulations"
        ]

        # Reject obvious non-resume documents
        for keyword in blocked_keywords:
            if keyword in text:
                raise ValueError(
                    "This document appears to be a letter, certificate, report or another non-resume document."
                )

        score = 0

        # Resume sections
        score += sum(section in text for section in resume_sections)

        # Email
        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text):
            score += 2

        # Phone number
        if re.search(r"\+?\d[\d\s\-()]{8,}", resume_text):
            score += 2

        # LinkedIn
        if "linkedin" in text:
            score += 1

        # GitHub
        if "github" in text:
            score += 1

        # Very low score → reject immediately
        if score < 5:
            raise ValueError(
                "This document doesn't appear to be a valid Resume/CV."
            )

        # ==================================================
        # AI VALIDATION
        # ==================================================

        validation = self.groq.validate_resume(resume_text)

        if not validation.get("is_resume", False):
            raise ValueError(
                validation.get(
                    "reason",
                    "The uploaded document is not a valid Resume/CV."
                )
            )

        # ==================================================
        # AI ANALYSIS
        # ==================================================

        analysis = self.groq.analyze_resume(resume_text)

        # Save JSON report
        self.file_handler.save_report(
            output_path,
            json.dumps(analysis, indent=4)
        )

        # Generate PDF report
        self.pdf.generate(
            analysis,
            "data/reports/resume_report.pdf"
        )

        return analysis