import os
import tempfile

import streamlit as st

from services.resume_service import ResumeService


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# LOAD CSS
# =====================================================

def load_css():

    with open("styles/style.css", "r", encoding="utf-8") as css_file:

        st.markdown(

            f"<style>{css_file.read()}</style>",

            unsafe_allow_html=True

        )


load_css()


# =====================================================
# INITIALIZE SERVICES
# =====================================================

resume_service = ResumeService()


# =====================================================
# HERO SECTION
# =====================================================

def render_hero():

    st.markdown(

        """
<div class="hero">

<div class="badge">
⚡ Powered by Groq • Llama 3.3 70B
</div>

<div class="title">
🤖 AI Resume Analyzer
</div>

<div class="subtitle">
Upload your resume and receive an AI-powered ATS analysis,
missing skills,
personalized feedback,
and professional improvement suggestions in seconds.
</div>

</div>
""",

        unsafe_allow_html=True

    )



# =====================================================
# FEATURES SECTION
# =====================================================

def render_features():

    st.markdown("""
<div class="features">

<div class="feature-pill">📊 ATS Score</div>

<div class="feature-pill">🧠 AI Feedback</div>

<div class="feature-pill">🎯 Missing Skills</div>

<div class="feature-pill">📄 PDF Report</div>

</div>
""", unsafe_allow_html=True)
    
    # =====================================================
# UPLOAD SECTION
# =====================================================

def render_upload():

    st.markdown("""
<div class="upload-card">

<div class="upload-icon">
📄
</div>

<h2>Upload Your Resume</h2>

<p>
Upload your resume in PDF or DOCX format and let AI analyze
your ATS score, strengths, weaknesses, and missing skills.
</p>

</div>
""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )

    return uploaded_file

# =====================================================
# MAIN
# =====================================================


render_hero()

render_features()

uploaded_file = render_upload()

if uploaded_file:

    if st.button("🚀 Analyze Resume", use_container_width=True):

        with st.spinner("🤖 AI is analyzing your resume..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp_file:

                tmp_file.write(uploaded_file.getbuffer())
                temp_path = tmp_file.name

            os.makedirs("data/reports", exist_ok=True)

            report_path = "data/reports/resume_analysis.json"

            try:
                analysis = resume_service.analyze_resume(
                    temp_path,
                    report_path
                )

            except ValueError as e:
                st.error(
                    f"❌ {str(e)}\n\nPlease upload a valid Resume or CV in PDF or DOCX format."
                )
                st.stop()

            except Exception:
                st.error("❌ Something went wrong while analyzing the resume.")
                st.stop()

            st.success("✅ Analysis Completed!")

            # ==========================
            # Download PDF Button
            # ==========================
         



            pdf_path = "data/reports/resume_report.pdf"

            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_file,
                        file_name="AI_Resume_Analysis_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📊 ATS Score",
                    f"{analysis.get('ats_score', 0)}%"
                )

            with col2:
                st.metric(
                    "💪 Strengths",
                    len(analysis.get("strengths", []))
                )

            with col3:
                st.metric(
                    "🎯 Missing Skills",
                    len(analysis.get("missing_skills", []))
                )

            st.divider()

            st.markdown(
                f"""
                <h3 style="color:white; margin-bottom:10px;">
                    📊 ATS Score: {analysis['ats_score']}/100
                </h3>
                """,
                unsafe_allow_html=True
            )

            st.progress(analysis["ats_score"] / 100)

            score = analysis["ats_score"]

            if score >= 90:
                st.success("🟢 Excellent Resume")

            elif score >= 75:
                st.info("🔵 Good Resume")

            elif score >= 60:
                st.warning("🟡 Average Resume")

            else:
                st.error("🔴 Needs Improvement")

            st.markdown("""
            <div class="result-card">
                <h2>📑 Resume Analysis</h2>
            </div>
            """, unsafe_allow_html=True)

            # ==========================
            # Strengths
            # ==========================

            st.markdown(
                '<div class="result-heading">💪 Strengths</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get("strengths", []):
                st.markdown(
                    f'<div class="result-item">✅ {item}</div>',
                    unsafe_allow_html=True
                )

            # ==========================
            # Weaknesses
            # ==========================

            st.markdown(
                '<div class="result-heading">⚠️ Weaknesses</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get("weaknesses", []):
                st.markdown(
                    f'<div class="result-item">❌ {item}</div>',
                    unsafe_allow_html=True
                )

            # ==========================
            # Missing Skills
            # ==========================

            st.markdown(
                '<div class="result-heading">🎯 Missing Skills</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get("missing_skills", []):
                st.markdown(
                    f'<div class="result-item">📌 {item}</div>',
                    unsafe_allow_html=True
                )

            # ==========================
            # Suggestions
            # ==========================

            st.markdown(
                '<div class="result-heading">💡 Suggestions</div>',
                unsafe_allow_html=True
            )

            for item in analysis.get("suggestions", []):
                st.markdown(
                    f'<div class="result-item">👉 {item}</div>',
                    unsafe_allow_html=True
                )

          