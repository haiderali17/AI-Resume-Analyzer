# 🤖 AI Resume Analyzer

An AI-powered Resume Analyzer built with **Python**, **Streamlit**, and **Google Gemini AI**. Upload your resume and receive intelligent feedback, ATS analysis, strengths, weaknesses, improvement suggestions, and a professionally formatted PDF report.

---

## ✨ Features

- 📄 Upload Resume (PDF/DOCX)
- 🤖 AI Resume Analysis using Google Gemini
- 📊 ATS-Friendly Resume Evaluation
- 💪 Strengths & Weaknesses Detection
- 💡 Personalized Improvement Suggestions
- 📥 Download Analysis Report as PDF
- 🎨 Clean and Responsive Streamlit Interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- PyMuPDF
- python-docx
- ReportLab
- python-dotenv

---

## 📂 Project Structure

```
ai_resume_analyzer/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── services/
│   ├── gemini_service.py
│   └── resume_service.py
│
├── utils/
│   ├── file_handler.py
│   ├── logger.py
│   └── pdf_generator.py
│
├── data/
│   ├── resumes/
│   └── reports/
│
└── logs/
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/haiderali17/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📷 Screenshots

You can add screenshots here after deployment.

---

## 📌 Future Improvements

- Resume Score (0–100)
- Job Description Matching
- Multiple Resume Comparison
- Dark Mode
- Resume Templates
- Cover Letter Generator

---

## 👨‍💻 Author

**Haider Ali**

BS Information Technology Student | AI & Machine Learning Enthusiast

GitHub:
https://github.com/haiderali17

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.