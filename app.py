import os
import tempfile
import streamlit as st
from services.resume_service import ResumeService
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

resume_service = ResumeService()

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

/* ===========================
   Background
=========================== */

.stApp{
    background:#eef2f7;
}

/* Main Container */
.block-container{
    background:white;
    padding:2.5rem;
    border-radius:18px;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    margin-top:30px;
    margin-bottom:30px;
}

/* Hide Streamlit Branding */
#MainMenu{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
header{
    visibility:hidden;
}

/* ===========================
   Typography
=========================== */

.main-title{
    text-align:center;
    font-size:44px;
    font-weight:700;
    color:#1f2937;
    margin-bottom:8px;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:#6b7280;
    margin-bottom:35px;
}

/* ===========================
   Upload Box
=========================== */

[data-testid="stFileUploader"]{
    border:2px dashed #cbd5e1;
    border-radius:14px;
    background:#f8fafc;
    padding:18px;
}

/* ===========================
   Buttons
=========================== */

.stButton>button{

    width:100%;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    font-size:16px;
    font-weight:600;
    padding:12px;

    transition:0.25s;
}

.stButton>button:hover{

    background:#1d4ed8;
    transform:translateY(-2px);

}

/* Download Button */

.stDownloadButton>button{

    width:100%;
    background:#16a34a;
    color:white;
    border:none;
    border-radius:10px;
    font-size:16px;
    font-weight:600;
    padding:12px;

}

.stDownloadButton>button:hover{

    background:#15803d;

}

/* ===========================
   ATS Score Card
=========================== */

[data-testid="metric-container"]{

    background:#f8fafc;

    border:1px solid #e5e7eb;

    border-radius:14px;

    padding:20px;

    box-shadow:0 3px 10px rgba(0,0,0,.05);

}

/* Progress */

.stProgress>div>div{

    background:#22c55e;

}

/* ===========================
   Result Cards
=========================== */

[data-testid="stVerticalBlockBorderWrapper"]{

    background:white;

    border-radius:14px;

    border:1px solid #e5e7eb;

    padding:16px;

    box-shadow:0 3px 10px rgba(0,0,0,.05);

}

/* Divider */

hr{
    margin-top:25px;
    margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="main-title">
📄 AI Resume Analyzer
</div>

<div class="subtitle">
Get an AI-powered ATS analysis of your resume using Google Gemini.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Feature Overview
# -----------------------------
with st.container(border=True):

    st.markdown("### ✨ What You'll Receive")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
- ✅ ATS Score
- ✅ Resume Strengths
- ✅ Missing Skills
""")

    with c2:
        st.markdown("""
- ✅ Weaknesses Detection
- ✅ Improvement Suggestions
- ✅ Downloadable PDF Report
""")

st.write("")

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)

# -----------------------------
# Analyze
# -----------------------------
if uploaded_file:

    st.success(f"✅ **{uploaded_file.name}** uploaded successfully.")

    if st.button("🚀 Analyze Resume", use_container_width=True):

        with st.spinner("🤖 Gemini AI is analyzing your resume..."):

            try:

                extension = os.path.splitext(uploaded_file.name)[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())
                    temp_path = temp_file.name

                analysis = resume_service.analyze_resume(
                    file_path=temp_path,
                    output_path="data/reports/report.txt"
                )

                score = analysis["ats_score"]

                st.success("🎉 Resume analyzed successfully!")

                st.divider()

                # -----------------------------
                # ATS Score
                # -----------------------------
                st.markdown("## 📊 ATS Score")

                left, center, right = st.columns([1, 2, 1])

                with center:

                    st.metric(
                        label="Overall Resume Score",
                        value=f"{score}/100"
                    )

                    st.progress(score / 100)

                st.divider()

                col1, col2 = st.columns(2, gap="large")

                # -----------------------------
                # Left Column
                # -----------------------------
                with col1:

                    with st.container(border=True):

                        st.subheader("💪 Strengths")

                        for item in analysis["strengths"]:
                            st.success(item)

                    st.write("")

                    with st.container(border=True):

                        st.subheader("🎯 Missing Skills")

                        for item in analysis["missing_skills"]:
                            st.error(item)

                # -----------------------------
                # Right Column
                # -----------------------------
                with col2:

                    with st.container(border=True):

                        st.subheader("⚠️ Weaknesses")

                        for item in analysis["weaknesses"]:
                            st.warning(item)

                    st.write("")

                    with st.container(border=True):

                        st.subheader("💡 Suggestions")

                        for item in analysis["suggestions"]:
                            st.info(item)

                st.divider()

                # -----------------------------
                # Download PDF
                # -----------------------------
                pdf_path = "data/reports/resume_report.pdf"

                if os.path.exists(pdf_path):

                    with open(pdf_path, "rb") as pdf_file:

                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_file,
                            file_name="AI_Resume_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

            except Exception as e:

                st.error(f"❌ {str(e)}")