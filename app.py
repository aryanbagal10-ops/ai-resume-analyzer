import streamlit as st

from resume_analyzer import (
    extract_text_from_pdf,
    detect_skills,
    compare_resume_with_job,
    calculate_resume_quality
)


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main-title {
    font-size: 45px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="main-title">🤖 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume and compare it with a job description'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------
# RESUME
# -----------------------------

st.subheader("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)


# -----------------------------
# JOB DESCRIPTION
# -----------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder="Paste the complete job description here..."
)


# -----------------------------
# BUTTON
# -----------------------------

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)


# -----------------------------
# ANALYSIS
# -----------------------------

if analyze_button:

    if uploaded_file is None:

        st.warning("⚠️ Please upload your resume PDF first.")

    elif not job_description.strip():

        st.warning("⚠️ Please paste a job description.")

    else:

        resume_text = extract_text_from_pdf(
            uploaded_file
        )

        if not resume_text.strip():

            st.error(
                "❌ Could not extract text from this PDF."
            )

        else:

            st.success(
                "✅ Resume analyzed successfully!"
            )

            # -----------------------------
            # SKILLS
            # -----------------------------

            resume_skills = detect_skills(
                resume_text
            )

            # -----------------------------
            # JOB MATCH
            # -----------------------------

            match_score, matched, missing = (
                compare_resume_with_job(
                    resume_text,
                    job_description
                )
            )

            # -----------------------------
            # RESUME QUALITY
            # -----------------------------

            quality_score, feedback = (
                calculate_resume_quality(
                    resume_text
                )
            )

            # -----------------------------
            # RESULTS
            # -----------------------------

            st.subheader(
                "📊 Resume Analysis"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "🎯 Job Match",
                    f"{match_score}%"
                )

            with col2:

                st.metric(
                    "📄 Resume Quality",
                    f"{quality_score}%"
                )

            with col3:

                st.metric(
                    "💻 Skills Found",
                    len(resume_skills)
                )

            # -----------------------------
            # JOB MATCH BAR
            # -----------------------------

            st.write(
                f"**Job Match: {match_score}%**"
            )

            st.progress(
                match_score / 100
            )

            # -----------------------------
            # RESUME QUALITY BAR
            # -----------------------------

            st.write(
                f"**Resume Quality: {quality_score}%**"
            )

            st.progress(
                quality_score / 100
            )

            # -----------------------------
            # SKILLS
            # -----------------------------

            st.subheader(
                "🧠 Skills Found in Resume"
            )

            if resume_skills:

                st.write(
                    " • ".join(resume_skills)
                )

            else:

                st.warning(
                    "No known technical skills detected."
                )

            # -----------------------------
            # MATCHED
            # -----------------------------

            st.subheader(
                "✅ Matched Skills"
            )

            if matched:

                for skill in matched:

                    st.success(
                        skill
                    )

            else:

                st.info(
                    "No matching skills found."
                )

            # -----------------------------
            # MISSING
            # -----------------------------

            st.subheader(
                "❌ Missing Skills"
            )

            if missing:

                for skill in missing:

                    st.error(
                        skill
                    )

            else:

                st.success(
                    "🎉 No missing job-related skills detected!"
                )

            # -----------------------------
            # FEEDBACK
            # -----------------------------

            st.subheader(
                "💡 Resume Improvement Suggestions"
            )

            if feedback:

                for item in feedback:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.success(
                    "🎉 Your resume has a strong basic structure!"
                )

            # -----------------------------
            # EXTRACTED TEXT
            # -----------------------------

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.write(
                    resume_text
                )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "Built with Python • Streamlit • PyPDF2 • GitHub"
)