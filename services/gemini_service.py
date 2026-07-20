import json
import time
from google import genai
from config import API_KEY
from utils.logger import logger


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
    
    # Analyze Resume
    def analyze_resume(self, resume_text: str) -> dict:

    # Prompt
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

        try:
            response = None
            for _ in range(3):
                try:
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    break
                except Exception:
                    time.sleep(3)

            if response is None:
                raise Exception("Gemini API is currently unavailable. Please try again.")

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:
                text = text[start:end + 1]

            result = json.loads(text)

            logger.info("Resume analyzed successfully.")

            return result

        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            raise