import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# 🔐 Load API key securely
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ⚙️ Model Configuration (lower temperature for consistent scoring)
configuration = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json"
}

# 🚀 Use Gemini 1.5 Pro for better structured reasoning
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=configuration
)

def analyse_resume_gemini(resume_content, job_description):
    """
    Analyzes a resume against a job description using Gemini.
    Returns structured JSON with score, breakdown, missing skills, suggestions, etc.
    """

    prompt = f"""
    You are a professional ATS (Applicant Tracking System) and resume analyzer.

    Resume:
    {resume_content}

    Job Description:
    {job_description}

    Task:
    1. Analyze the resume against the job description.
    2. Use the following **rubric with weightage** to calculate the match score (total = 100):
       - Technical Skills Match: 40%
       - Work Experience & Projects Relevance: 30%
       - Education & Certifications: 15%
       - Soft Skills / Communication / Teamwork: 10%
       - Additional Achievements: 5%
    3. Show the score breakdown per category.
    4. List missing/weak skills and experiences.
    5. Suggest improvements to align resume with the role.
    6. Provide additional tailored suggestions based on company type:
       - Service-based → focus on client communication, multiple tech-stack exposure, delivery, teamwork.
       - Product-based → focus on problem-solving, system design, scalability, performance optimization, ownership.
    7. Create a **skills comparison table** (existing vs missing skills).

    📌 IMPORTANT: Return the result ONLY in **valid JSON format** with this schema:
    {{
      "match_score": "XX/100",
      "score_breakdown": {{
        "technical_skills": "XX/40",
        "experience": "XX/30",
        "education": "XX/15",
        "soft_skills": "XX/10",
        "achievements": "XX/5"
      }},
      "missing_skills": ["skill1", "skill2", "..."],
      "suggestions": ["suggestion1", "suggestion2", "..."],
      "company_alignment": {{
        "service_based": "tips for service-based",
        "product_based": "tips for product-based"
      }},
      "summary": "2–3 sentence evaluation",
      "skills_table": [
        {{
          "category": "Technical",
          "existing": ["..."],
          "missing": ["..."]
        }},
        {{
          "category": "Experience",
          "existing": ["..."],
          "missing": ["..."]
        }},
        {{
          "category": "Education",
          "existing": ["..."],
          "missing": ["..."]
        }},
        {{
          "category": "Soft Skills",
          "existing": ["..."],
          "missing": ["..."]
        }},
        {{
          "category": "Achievements",
          "existing": ["..."],
          "missing": ["..."]
        }}
      ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)  # ✅ Parse JSON directly
    except Exception as e:
        return {"error": str(e)}
