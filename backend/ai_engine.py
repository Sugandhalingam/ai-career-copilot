import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an expert career coach and resume analyst.

    Analyze the following resume against the job description provided.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Provide your analysis in exactly this format:

    OVERALL SCORE: (give a score out of 100)

    STRENGTHS:
    - (list what the resume does well compared to the job)

    MISSING SKILLS:
    - (list exact skills/tools mentioned in job but missing from resume)

    IMPROVEMENTS:
    - (list specific changes to make the resume stronger)

    VERDICT:
    (2-3 lines summary of overall fit for this role)
    """
    return ask_ai(prompt)


def get_skill_roadmap(missing_skills, job_title):
    prompt = f"""
    You are an expert learning coach.

    A person wants to become a {job_title}.
    They are missing these skills: {missing_skills}

    Create a week by week learning roadmap to help them gain these skills.

    Provide your roadmap in exactly this format:

    ROADMAP FOR: {job_title}

    WEEK 1:
    - Skill to learn:
    - What to study:
    - Free resource:

    WEEK 2:
    - Skill to learn:
    - What to study:
    - Free resource:

    (continue for as many weeks as needed, maximum 6 weeks)

    FINAL TIP:
    (one motivating and practical tip for this person)
    """
    return ask_ai(prompt)


def generate_interview_questions(resume_text, job_description, job_title):
    prompt = f"""
    You are an experienced technical interviewer.

    Based on this resume and job description, generate a mock interview for the role of {job_title}.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Generate exactly 5 interview questions. Focus on the candidate's weak areas and the job requirements.

    Provide in exactly this format:

    MOCK INTERVIEW FOR: {job_title}

    Q1: (question)
    WHAT THEY'RE TESTING: (what skill or quality this question tests)
    IDEAL ANSWER HINT: (what a good answer should include)

    Q2: (question)
    WHAT THEY'RE TESTING:
    IDEAL ANSWER HINT:

    Q3: (question)
    WHAT THEY'RE TESTING:
    IDEAL ANSWER HINT:

    Q4: (question)
    WHAT THEY'RE TESTING:
    IDEAL ANSWER HINT:

    Q5: (question)
    WHAT THEY'RE TESTING:
    IDEAL ANSWER HINT:
    """
    return ask_ai(prompt)