import json
from groq import Groq
from config import GROQ_API_KEY
from utils.logger import logger


class GroqService:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    # -----------------------------
    # Resume Validation
    # -----------------------------
    def validate_resume(self, resume_text: str) -> dict:

        prompt = f"""
You are an expert HR document classifier.

Your ONLY job is to determine whether the uploaded document is an actual Resume/CV.

A valid Resume/CV is a document created by a candidate to present their qualifications for a job.

A Resume/CV usually contains MOST of these sections:
- Candidate Name
- Contact Information
- Email
- Phone Number
- Skills
- Education
- Work Experience
- Projects
- Certifications
- Achievements
- Technical Skills

The following are NOT resumes:
- Internship Offer Letter
- Internship Completion Letter
- Appointment Letter
- Joining Letter
- Offer Letter
- Experience Certificate
- Recommendation Letter
- Character Certificate
- Degree Certificate
- Research Paper
- Assignment
- Article
- Book
- Invoice
- Receipt
- Bank Statement
- Government Letter
- Legal Document
- Any letter beginning with "Dear"
- Any document congratulating or offering a position

Return ONLY valid JSON.

If the document is NOT a Resume/CV:

{{
    "is_resume": false,
    "confidence": 0,
    "reason": "The uploaded document is not a Resume/CV."
}}

If it IS a Resume/CV:

{{
    "is_resume": true,
    "confidence": 95,
    "reason": "The uploaded document is a Resume/CV."
}}

Document:

{resume_text}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("AI returned an invalid response during resume validation.")

        text = text[start:end + 1]

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI validation response.")

        logger.info("Resume validation completed.")

        return result

    # -----------------------------
    # Resume Analysis
    # -----------------------------
    def analyze_resume(self, resume_text: str) -> dict:

        prompt = f"""
You are an ATS Resume Expert.

Analyze ONLY valid resumes.

Return ONLY valid JSON.

{{
    "ats_score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": []
}}

Rules:
- Return ONLY valid JSON.
- ATS Score must be between 0 and 100.

Resume:

{resume_text}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("AI returned an invalid response during resume analysis.")

        text = text[start:end + 1]

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI analysis response.")

        logger.info("Resume analyzed successfully.")

        return result