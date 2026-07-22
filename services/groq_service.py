import json
from groq import Groq
from config import GROQ_API_KEY
from utils.logger import logger


class GroqService:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    # -----------------------------
    # Resume / CV Validation
    # -----------------------------
    def validate_resume(self, resume_text: str) -> dict:

        prompt = f"""
You are an expert HR document classifier.

Your task is to determine whether the uploaded document is intended to present a person's qualifications for employment, internships, freelance work, higher education, or academic opportunities.

Treat BOTH resumes and CVs as VALID.

A valid Resume/CV may belong to:
- Student
- Fresh Graduate
- Experienced Professional
- Career Changer
- Freelancer
- Researcher
- Academic

A Resume/CV DOES NOT need every standard section.

It may contain only a few of these:
- Name
- Contact Information
- Email
- Phone Number
- LinkedIn / Portfolio
- Objective / Summary
- Education
- Skills
- Technical Skills
- Projects
- Experience
- Internships
- Certifications
- Achievements
- Research
- Publications
- Awards
- Languages

Accept different layouts and writing styles.

Return is_resume = false ONLY if the document is clearly NOT a Resume/CV.

Examples of invalid documents:
- Offer Letter
- Appointment Letter
- Joining Letter
- Internship Letter
- Experience Certificate
- Character Certificate
- Degree Certificate
- Invoice
- Receipt
- Bank Statement
- Government Document
- Legal Document
- Assignment
- Book
- Article
- Research Paper
- Advertisement
- Empty Document
- Corrupted / unreadable text

Return ONLY valid JSON.

If NOT Resume/CV:

{{
    "is_resume": false,
    "confidence": 95,
    "reason": "The uploaded document is not a Resume or CV."
}}

If Resume/CV:

{{
    "is_resume": true,
    "confidence": 95,
    "reason": "The uploaded document is a valid Resume or CV."
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
            raise ValueError("AI returned an invalid response during Resume/CV validation.")

        text = text[start:end + 1]

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI validation response.")

        logger.info("Resume/CV validation completed.")

        return result

    # -----------------------------
    # Resume / CV Analysis
    # -----------------------------
    def analyze_resume(self, resume_text: str) -> dict:

        prompt = f"""
You are a Senior HR Recruiter, ATS Expert, and Career Coach.

Analyze the uploaded Resume or CV professionally.

Treat BOTH resumes and CVs as valid.

Do NOT reject a Resume/CV because:
- It belongs to a student
- It belongs to a fresher
- It has no work experience
- It is an academic CV
- It contains projects instead of experience

If experience is missing, evaluate:
- Education
- Projects
- Skills
- Certifications
- Achievements
- Technical Strength

Evaluate the Resume/CV based on:

1. ATS Compatibility
2. Skills
3. Technical Skills
4. Projects
5. Experience (if available)
6. Education
7. Certifications
8. Overall Presentation

ATS Score Guidelines

90-100
Outstanding

75-89
Strong

60-74
Average

40-59
Needs Improvement

Below 40
Very Weak

Provide practical and constructive feedback.

Return ONLY valid JSON.

Format:

{{
    "ats_score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": []
}}

Rules:

- Return ONLY JSON.
- ATS score must be between 0 and 100.
- Give at least 3 strengths whenever possible.
- Give at least 3 weaknesses if applicable.
- Give realistic missing skills.
- Suggestions must be practical and actionable.
- Do not invent fake experience.
- Do not criticize missing experience for students if they have projects.
- Evaluate fairly.

Resume/CV:

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
            raise ValueError("AI returned an invalid response during Resume/CV analysis.")

        text = text[start:end + 1]

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI analysis response.")

        logger.info("Resume/CV analyzed successfully.")

        return result