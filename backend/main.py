from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import os
from analyze_pdf import analyse_resume_gemini

app = FastAPI(title="Resume Analyzer API")

# ✅ Allow CORS (so frontend like React/Streamlit can access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set ["http://localhost:3000"] for React dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Utility: Extract text from PDF
def extract_text_from_resume(file_path: str):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 📌 Root route
@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running 🚀"}

# 📌 API: Upload Resume + JD
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile,
    job_description: str = Form(...)
):
    try:
        # Save uploaded resume temporarily
        file_location = f"/tmp/{resume.filename}"
        with open(file_location, "wb") as f:
            f.write(await resume.read())

        # Extract text
        resume_content = extract_text_from_resume(file_location)

        # Run Gemini analysis
        result = analyse_resume_gemini(resume_content, job_description)

        return {"status": "success", "data": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}
