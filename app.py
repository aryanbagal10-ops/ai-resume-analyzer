import streamlit as st

from resume_analyzer import (
    extract_text_from_pdf,
    detect_skills,
    compare_resume_with_job
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 650;
    margin-top: 30px;
}

.skill-box {
    padding: 10px 15px;
    border-radius: 10px;
    margin: 5px 0;
    background-color: #f5f7fa;
    border: 1px solid #e2e5e9;
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 50px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume and compare it with a job description using AI-powered skill matching.'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your Resume PDF",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Example:\n"
            "We are looking for a Python Developer with "
            "knowledge of Python, SQL, Pandas, NumPy..."
        )
    )


st.write("")


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

analyze = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)


if analyze:

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume PDF first."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please paste a job description first."
        )

    else:

        # --------------------------------------------------
        # EXTRACT RESUME TEXT
        # --------------------------------------------------

        with st.spinner("🔄 Analyzing your resume..."):

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        if not resume_text.strip():

            st.error(
                "❌ Could not extract text from this PDF. "
                "Please upload a text-based PDF."
            )

        else:

            st.success(
                "✅ Resume analyzed successfully!"
            )


            # --------------------------------------------------
            # ANALYSIS
            # --------------------------------------------------

            resume_skills = detect_skills(
                resume_text
            )

            score, matched, missing = (
                compare_resume_with_job(
                    resume_text,
                    job_description
                )
            )


            # --------------------------------------------------
            # SCORE
            # --------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '📊 Resume Match Analysis'
                '</div>',
                unsafe_allow_html=True
            )

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


            # Progress bar

            st.progress(
                score / 100,
                text=f"Resume Match: {score}%"
            )


            # --------------------------------------------------
            # SKILLS FOUND
            # --------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '🧠 Skills Found in Resume'
                '</div>',
                unsafe_allow_html=True
            )


            if resume_skills:

                skills_text = " • ".join(
                    resume_skills
                )

                st.info(
                    skills_text
                )

            else:

                st.warning(
                    "No known skills were detected."
                )


            # --------------------------------------------------
            # MATCHED SKILLS
            # --------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '✅ Matched Skills'
                '</div>',
                unsafe_allow_html=True
            )


            if matched:

                for skill in matched:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No matching skills found."
                )


            # --------------------------------------------------
            # MISSING SKILLS
            # --------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '❌ Missing Skills'
                '</div>',
                unsafe_allow_html=True
            )


            if missing:

                for skill in missing:

                    st.warning(
                        f"• {skill}"
                    )

            else:

                st.success(
                    "🎉 No major missing skills detected!"
                )


            # --------------------------------------------------
            # SUGGESTIONS
            # --------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '💡 Resume Improvement Suggestions'
                '</div>',
                unsafe_allow_html=True
            )


            if missing:

                st.write(
                    "Consider learning these skills "
                    "and adding relevant projects or "
                    "experience to your resume:"
                )

                for skill in missing:

                    st.write(
                        f"👉 Learn / demonstrate **{skill}**"
                    )

            else:

                st.success(
                    "Your detected skills match the "
                    "job requirements well."
                )


            # --------------------------------------------------
            # EXTRACTED TEXT
            # --------------------------------------------------

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text(
                    resume_text
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="footer">'
    '🤖 AI Resume Analyzer • Built with Python + Streamlit'
    '</div>',
    unsafe_allow_html=True
)