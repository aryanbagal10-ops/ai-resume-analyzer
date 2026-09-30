import streamlit as st

from resume_analyzer import (
    extract_text_from_pdf,
    detect_skills,
    compare_resume_with_job
)


# Page settings
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# Title
st.title("🤖 AI Resume Analyzer")

st.write(
    "Upload your resume and compare it with a job description."
)


# Resume upload
uploaded_file = st.file_uploader(
    "📄 Upload your Resume PDF",
    type=["pdf"]
)


# Job description
job_description = st.text_area(
    "💼 Paste Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)


# Analyze button
if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:
        st.warning("Please upload a PDF resume.")

    elif not job_description.strip():
        st.warning("Please paste a job description.")

    else:

        # Extract resume text
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text.strip():
            st.error(
                "Could not extract text from this PDF. "
                "Please use a text-based PDF."
            )

        else:

            st.success("Resume analyzed successfully! 🎉")


            # Detect skills
            resume_skills = detect_skills(resume_text)


            # Compare resume with job
            score, matched, missing = compare_resume_with_job(
                resume_text,
                job_description
            )


            # Results
            st.subheader("📊 Resume Analysis")


            col1, col2, col3 = st.columns(3)


            with col1:
                st.metric(
                    "🎯 Match Score",
                    f"{score}%"
                )


            with col2:
                st.metric(
                    "✅ Matched Skills",
                    len(matched)
                )


            with col3:
                st.metric(
                    "❌ Missing Skills",
                    len(missing)
                )


            # Detected skills
            st.subheader("🧠 Skills Found in Resume")

            if resume_skills:

                st.write(", ".join(resume_skills))

            else:

                st.info("No known skills detected.")


            # Matched skills
            st.subheader("✅ Matched Skills")

            if matched:

                for skill in matched:
                    st.write(f"✓ {skill}")

            else:

                st.write("No matching skills found.")


            # Missing skills
            st.subheader("❌ Missing Skills")

            if missing:

                for skill in missing:
                    st.write(f"• {skill}")

            else:

                st.success(
                    "No major missing skills detected!"
                )


            # Suggestions
            st.subheader("💡 Suggestions")

            if missing:

                st.write(
                    "Consider learning or demonstrating "
                    "these skills in your projects:"
                )

                for skill in missing:
                    st.write(f"👉 {skill}")

            else:

                st.success(
                    "Your detected skills match the "
                    "job requirements well."
                )


            # Resume text
            with st.expander("📄 View Extracted Resume Text"):

                st.text(resume_text)