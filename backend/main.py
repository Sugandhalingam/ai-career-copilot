from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pdf_reader import extract_text_from_pdf
from ai_engine import analyze_resume, get_skill_roadmap, generate_interview_questions

app = FastAPI()

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/ui")
def serve_ui():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# This allows our React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route - just to check if server is running
@app.get("/")
def home():
    return {"message": "AI Career Copilot backend is running!"}


# Route 1 - Resume Analysis
@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(...)
):
    # Save uploaded PDF temporarily
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_path)

    # Send to AI for analysis
    analysis = analyze_resume(resume_text, job_description)

    # Clean up uploaded file
    os.remove(file_path)

    return {"analysis": analysis}


# Route 2 - Skill Roadmap
@app.post("/roadmap")
async def roadmap(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(...)
):
    # Save uploaded PDF temporarily
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_path)

    # Get analysis first to find missing skills
    analysis = analyze_resume(resume_text, job_description)

    # Generate roadmap based on missing skills
    skill_roadmap = get_skill_roadmap(analysis, job_title)

    # Clean up uploaded file
    os.remove(file_path)

    return {"roadmap": skill_roadmap}


# Route 3 - Mock Interview
@app.post("/interview")
async def interview(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(...)
):
    # Save uploaded PDF temporarily
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    resume_text = extract_text_from_pdf(file_path)

    # Generate interview questions
    questions = generate_interview_questions(resume_text, job_description, job_title)

    # Clean up uploaded file
    os.remove(file_path)

    return {"interview": questions}