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

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

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

    matched = sorted(
        resume_skills.intersection(job_skills)
    )

    missing = sorted(
        job_skills - resume_skills
    )

    return score, matched, missing


def calculate_resume_quality(resume_text):

    text = resume_text.lower()

    score = 0
    feedback = []

    # Contact information
    if re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text):
        score += 10
    else:
        feedback.append("Add a professional email address.")

    # Education
    if any(word in text for word in [
        "education",
        "b.tech",
        "btech",
        "degree",
        "college",
        "university"
    ]):
        score += 15
    else:
        feedback.append("Add a clear Education section.")

    # Skills
    skills = detect_skills(text)

    if len(skills) >= 8:
        score += 20
    elif len(skills) >= 5:
        score += 15
    elif len(skills) >= 3:
        score += 10
    else:
        feedback.append("Add more relevant technical skills.")

    # Projects
    if any(word in text for word in [
        "project",
        "projects"
    ]):
        score += 20
    else:
        feedback.append("Add at least 2 practical projects.")

    # GitHub
    if "github" in text:
        score += 10
    else:
        feedback.append("Add your GitHub profile or project links.")

    # LinkedIn
    if "linkedin" in text:
        score += 10
    else:
        feedback.append("Add your LinkedIn profile.")

    # Experience / internship
    if any(word in text for word in [
        "internship",
        "intern",
        "experience"
    ]):
        score += 10
    else:
        feedback.append(
            "Add internship, hackathon or practical experience when available."
        )

    # Resume length/content
    if len(text.split()) >= 250:
        score += 5
    else:
        feedback.append(
            "Add more meaningful project and achievement details."
        )

    return min(score, 100), feedback