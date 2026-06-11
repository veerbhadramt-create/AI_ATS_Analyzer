# AI ATS Resume Optimizer & Analyzer

An advanced, premium-design AI-powered ATS (Applicant Tracking System) Resume Analyzer built entirely in **Python** using **Streamlit** and the official **Google Gemini API**. 

This application parses resumes, extracts content, analyzes them against specific job descriptions, and calculates matching scores, highlights missing keywords, identifies strengths, and provides actionable recommendations to optimize application success.

---

## 🌟 Key Features

- **📄 Dynamic PDF Parsing**: Drag-and-drop or select any `.pdf` resume file to automatically extract text locally using the `pypdf` module.
- **✍️ Manual Text Input Option**: Paste resume details directly or modify extracted text in real-time.
- **📊 ATS Scoring Dashboard**: A beautiful, animated custom SVG radial gauge score indicator that dynamically changes color based on match levels:
  - 🟢 **80+**: Good/Excellent Match
  - 🟡 **60-79**: Moderate Match
  - 🔴 **Below 60**: Needs Improvement
- **🏷️ Keyword Identification**: Detects critical skills, terms, and tools mentioned in the Job Description but missing from your resume.
- **⚡ Actionable Recommendations**: Detailed recommendations to optimize resume layouts, formatting, and wording.
- **💪 Match Strengths**: Highlights where your resume aligns exceptionally well with the job listing.
- **🧪 Interactive Demo Mode**: Switch to "Demo Mode" instantly to show simulated analysis reports using real developer data, removing the friction of entering API keys during showcases.
- **🔒 API Privacy**: Your Gemini API key is stored securely in streamlit session state/local browser and is never cached in any external database.

---

## 🛠️ Technology Stack

- **Frontend & Backend UI**: Streamlit (Python Web Application framework)
- **AI Core Engine**: Google Gemini 1.5 Flash (via official `google-generativeai` SDK)
- **PDF Text Processing**: `pypdf`
- **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started (Run Locally)

### 1. Clone or Open the Directory
Open your terminal inside this project folder:
```bash
cd AI_ATS_Resume_Analyzer
```

### 2. Install Dependencies
Install all required libraries using:
```bash
pip install -r requirements.txt
```

### 3. Run the App
Start the Streamlit development server:
```bash
streamlit run app.py
```
*(Alternatively, you can run `streamlit run Atsresume..py`)*

The server will spin up and open `http://localhost:8501` automatically in your browser.

---

## 🌍 How to Deploy (Netlify or Streamlit Cloud)

### Option 1: Streamlit Community Cloud (Recommended & Instant for Python)
1. Push this codebase to a public GitHub repository.
2. Go to [Streamlit Share](https://share.streamlit.io/).
3. Connect your GitHub account, select this repo, and choose `app.py` as the main entry point.
4. Click **Deploy**. Your app will be live with a shareable URL in 2 minutes!

---

## 🎓 Interview Prep Cheat Sheet (For recruiters & hiring managers)

### 1. Problem Statement
> *"Many candidates fail recruiter screening stages because applicant tracking systems (ATS) discard resumes that lack specific keywords, even if the candidate is qualified. My app helps candidates find gaps and optimize their resume to beat these screening algorithms."*

### 2. Why Python and Streamlit?
> *"I selected Python and Streamlit because they allowed me to create a fully working AI tool with an elegant, responsive interface in record time, without the overhead of JavaScript build configurations. It lets me focus 100% on the core AI integration, PDF text parsing, and analytical layout."*

### 3. AI Decisions & Prompt Engineering
> *"I leveraged the Gemini 1.5 Flash model because of its high context window and speed. I configured it to return a structured JSON string by setting the `response_mime_type` to `application/json` in the configuration. This guarantees that the response conforms to my custom schema, making UI card rendering 100% crash-free."*

### 4. Technical Challenges Overcome
> *"A primary challenge was ensuring the app was testable for interviewers who didn't want to sign up for Google AI Studio keys. I designed a toggleable 'Demo Mode' that bypasses the live API call and returns a high-fidelity simulated analysis, demonstrating the complete UI flow and SVG progress gauges instantly."*
