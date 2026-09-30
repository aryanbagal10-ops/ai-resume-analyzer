import PyPDF2
import re


SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "react",
    "node.js",
    "flask",
    "django",
    "streamlit",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch"
]


def extract_text_from_pdf(uploaded_file):
    text = ""

    reader = PyPDF2.PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def detect_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def compare_resume_with_job(resume_text, job_description):
    resume_skills = set(detect_skills(resume_text))
    job_skills = set(detect_skills(job_description))

    if len(job_skills) == 0:
        score = 0
    else:
        score = int(
            len(resume_skills.intersection(job_skills))
            / len(job_skills)
            * 100
        )

    matched = sorted(resume_skills.intersection(job_skills))
    missing = sorted(job_skills - resume_skills)

    return score, matched, missing
