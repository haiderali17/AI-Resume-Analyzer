import json
from groq import Groq
from config import GROQ_API_KEY
from utils.logger import logger


class GroqService:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def analyze_resume(self, resume_text: str) -> dict:

        prompt = f"""
You are an ATS Resume Expert.

Analyze the following resume.

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
- Do NOT use markdown.
- Do NOT explain anything.
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
            text = text.replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}")

        text = text[start:end+1]

        result = json.loads(text)

        logger.info("Resume analyzed successfully.")

        return result