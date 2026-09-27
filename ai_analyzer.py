import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_resume(resume_text, job_description):
    if not API_KEY:
        return {"error": "GEMINI_API_KEY is missing. Add it to your .env file."}

    try:
        client = genai.Client(api_key=API_KEY)

        prompt = f"""
You are an expert resume and job-description analyzer.

Compare the RESUME with the JOB DESCRIPTION.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON using exactly this structure:
{{
  "match_score": 0,
  "matching_skills": [],
  "missing_skills": [],
  "recommended_keywords": [],
  "suggestions": []
}}

Rules:
- match_score must be a number from 0 to 100.
- matching_skills: important skills appearing in both.
- missing_skills: important job skills absent from the resume.
- recommended_keywords: useful job-description keywords the candidate could truthfully consider adding if applicable.
- suggestions: practical resume improvement suggestions.
- Do not invent candidate experience.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        raw = response.text.strip()
        raw = re.sub(r"^```json\s*|^```\s*|\s*```$", "", raw).strip()

        return json.loads(raw)

    except json.JSONDecodeError:
        return {"error": "Gemini returned an invalid JSON response. Please try again."}
    except Exception as error:
        return {"error": f"AI analysis failed: {error}"}
