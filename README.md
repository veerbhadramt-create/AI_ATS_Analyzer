# 🎯 AI ATS Resume Optimizer & Analyzer

[![Streamlit App](https://static.streamlit.io/badge-hosted-badge.svg)](https://aiatsanalyzer-a2e2n8mgoatzet8spk4fm7.streamlit.app/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A premium, interactive AI-powered Applicant Tracking System (ATS) Resume Analyzer. This application leverages the power of **Google Gemini API** to analyze, score, and optimize resumes against job descriptions, helping job seekers bridge keyword gaps and stand out to recruiters.

🔗 **Live Link:** [https://aiatsanalyzer-a2e2n8mgoatzet8spk4fm7.streamlit.app/](https://aiatsanalyzer-a2e2n8mgoatzet8spk4fm7.streamlit.app/)

---

## 🌟 Key Features

*   **📄 Intelligent PDF Parser:** Drag-and-drop or select any `.pdf` resume file to automatically extract text locally using the `pypdf` library.
*   **✍️ Real-Time Editing:** Adjust extracted resume content dynamically before initiating AI analysis.
*   **📊 Dynamic ATS Scoring Dashboard:** Custom-built SVG radial gauge score indicator that dynamically changes color based on match level:
    *   🟢 **80+ Score:** Strong Match (Ready for submission)
    *   🟡 **60-79 Score:** Moderate Match (Needs minor keyword optimization)
    *   🔴 **Below 60 Score:** Low Match (Needs significant alignment)
*   **🏷️ Intelligent Keyword Analysis:** Extracts critical skills, certifications, and technologies missing from your resume compared to the job description.
*   **⚡ Recruiter Feedback:** Generates structured summary reports simulating a recruiter's evaluation.
*   **💡 Actionable Recommendations:** Pinpoints exact revisions needed to elevate your resume score.

---

## 🎨 Theme & UI Design

*   **Wheat & Light Theme:** Beautiful, warm, and highly readable light cream aesthetic (`#FCFAF7` background) with rich brown typography (`#3E2723` & `#5D4037`) for a premium professional feel.
*   **Glassmorphism Cards:** Soft translucent cards with gentle shadows and golden-wheat borders.
*   **Responsive Control Panel:** Customized Streamlit widgets, file dropzones, and text fields custom-styled to fit the theme seamlessly.

---

## 🛠️ Technology Stack

*   **Frontend & UI:** Python, Streamlit, Custom CSS Injection
*   **AI Engine:** Google Gemini 1.5 Flash (via `google-generativeai`)
*   **Document Parsing:** `pypdf` (local file extraction)
*   **Environment Management:** `python-dotenv`

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.8 or higher installed.

### 1. Clone the Repository
```bash
git clone https://github.com/veerbhadramt-create/AI_ATS_Analyzer.git
cd AI_ATS_Analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
python -m streamlit run app.py
```
Your local server will boot up and automatically launch at `http://localhost:8501`.

---

## 🎓 Recruiter & Interview Cheat Sheet

### 1. System Architecture & Flow
The user uploads a PDF resume which is parsed locally using Python's `pypdf` library. The extracted text is combined with the user's targeted job description and sent to the Gemini 1.5 Flash model with a strictly structured prompt requesting JSON output. The app parses the JSON and renders it into a custom styled dashboard featuring custom SVG charts.

### 2. Prompt Engineering & Reliability
To ensure the application never crashes, Gemini is instructed to output a raw JSON structure matching a precise schema. We parse this output cleanly and handle exceptions gracefully, showing clear debugging suggestions if the API call fails.

### 3. Design decisions
Standard Streamlit applications look generic. In this project, custom CSS is injected to implement a premium **Wheat & Light Theme** using CSS variables, creating an eye-catching, responsive interface that feels like a standalone modern SaaS application.
