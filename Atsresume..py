import streamlit as st
import os
import json
import time
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# Load key from .env file
load_dotenv()

# Set up page
st.set_page_config(
    page_title="AI ATS Resume Optimizer",
    page_icon="🎯",
    layout="wide"
)

# Initialize theme session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Create a toggle on top left
toggle_col, _ = st.columns([3, 7])
with toggle_col:
    theme_toggle = st.toggle("🌙 Dark Mode" if st.session_state.theme == "dark" else "☀️ Light Mode", value=(st.session_state.theme == "light"), key="theme_toggle")
    st.session_state.theme = "light" if theme_toggle else "dark"

# Load the CSS file (Simple beginner file reading)
try:
    css_file = open("style.css", "r", encoding="utf-8")
    css_styles = css_file.read()
    css_file.close()
    st.markdown(f"<style>{css_styles}</style>", unsafe_allow_html=True)
except:
    st.warning("Could not load style.css file.")

# Inject light theme variables and additional styles if theme is light
if st.session_state.theme == "light":
    st.markdown("""
        <style>
        :root {
            --bg-color: #F8FAFC;
            --bg-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.06) 0px, transparent 50%),
                        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.04) 0px, transparent 50%);
            --text-color: #1E293B;
            
            --card-bg: rgba(255, 255, 255, 0.85);
            --card-border: rgba(0, 0, 0, 0.08);
            --card-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
            --card-header-color: #0F172A;
            --card-header-border: rgba(0, 0, 0, 0.08);
            
            --tagline-color: #475569;
            
            --sidebar-bg: #F1F5F9;
            --sidebar-border: rgba(0, 0, 0, 0.08);
            
            --result-bg: rgba(0, 0, 0, 0.02);
            --result-border: rgba(0, 0, 0, 0.06);
            --result-text: #334155;
            
            --svg-track: rgba(0, 0, 0, 0.06);
            --svg-text: #0F172A;
            --svg-subtext: rgba(0, 0, 0, 0.5);
            --score-title-color: rgba(15, 23, 42, 0.7);

            --input-bg: #ffffff;
            --input-border: rgba(0, 0, 0, 0.18);
            --input-text: #000000;
        }
        /* Extra theme overrides for Streamlit controls in Light Mode */
        .stMarkdown p, .stMarkdown span, label, p, span, .stTabs button {
            color: #1E293B !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] li {
            color: #1E293B !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(0, 0, 0, 0.03) !important;
            border-radius: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #475569 !important;
        }
        .stTabs [aria-selected="true"] {
            color: #4F46E5 !important;
            font-weight: 600 !important;
        }
        /* File uploader styling for light mode */
        [data-testid="stFileUploaderDropzone"] {
            background-color: rgba(0, 0, 0, 0.02) !important;
            border: 1px dashed rgba(0, 0, 0, 0.15) !important;
        }
        [data-testid="stFileUploaderDropzone"] p, [data-testid="stFileUploaderDropzone"] span {
            color: #475569 !important;
        }
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: rgba(0, 0, 0, 0.02) !important;
            color: #1E293B !important;
            border-radius: 8px;
        }
        /* Explicitly force dark text inside input elements for Light mode */
        input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def extract_text_from_pdf(pdf_file):
    # Beginner-friendly PDF text reader
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text != None:
                text = text + page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error("Error reading PDF file")
        return None


def analyze_resume_gemini(api_key, resume_text, job_desc):
    try:
        # Set up Gemini (strip spaces)
        genai.configure(api_key=api_key.strip())
        
        # Simple prompt
        prompt = f"""
        Analyze the following resume against the job description.
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_desc}
        
        Return the result as a raw JSON object. Do not include markdown code blocks.
        The JSON must contain these exact keys:
        - "score": (number out of 100)
        - "rating": (string, e.g. "Good Match")
        - "missing_keywords": (list of missing skills)
        - "strengths": (list of positive matches)
        - "suggestions": (list of recommendations)
        - "feedback": (short overall feedback text)
        """
        
        # Try gemini-2.5-flash first, fallback to gemini-2.0-flash and gemini-3.5-flash
        e1_err = None
        e2_err = None
        
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
        except Exception as e1:
            e1_err = e1
            try:
                # Try gemini-2.0-flash as first fallback
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
            except Exception as e2:
                e2_err = e2
                # Try gemini-3.5-flash as last resort
                model = genai.GenerativeModel("gemini-3.5-flash")
                response = model.generate_content(prompt)
        
        # Simple JSON loading with basic code-block stripping fallback
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            
        result = json.loads(raw_text)
        return result
        
    except Exception as e:
        st.error(f"Error running AI analysis: {str(e)}")
        if e1_err is not None:
            st.warning(f"gemini-2.5-flash failed with: {str(e1_err)}")
        if e2_err is not None:
            st.warning(f"gemini-2.0-flash failed with: {str(e2_err)}")
            
        try:
            # Check if key can list models (verifies key validity)
            available = []
            for m in genai.list_models():
                available.append(m.name.split("/")[-1])
            st.info(f"Debug Info - Models available on your API key: {available}")
        except Exception as key_err:
            st.error(f"API Key Verification Failed: {str(key_err)}")
            st.warning("Please verify that your Google AI Studio API key is correct and active.")
        return None


# --- Sidebar ---
st.sidebar.title("ATS Optimizer")
st.sidebar.write("Configure your settings below")

# Get API key
default_key = os.environ.get("GEMINI_API_KEY", "")
api_key_input = st.sidebar.text_input(
    "Enter Gemini API Key",
    value=default_key,
    type="password"
)

st.sidebar.write("### Instructions:")
st.sidebar.write("1. Upload your resume (PDF)")
st.sidebar.write("2. Paste the Job Description")
st.sidebar.write("3. Click Analyze!")


# --- Main Page UI ---
st.markdown("<h1 class='gradient-title'>Get Your Resume Shortlisted. Beat ATS.</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Optimize your resume keywords and get noticed by recruiters.</p>", unsafe_allow_html=True)

# Columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="glass-card">
            <div class="card-header">
                Resume Input
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for uploading file or pasting text
    tab1, tab2 = st.tabs(["📄 Upload PDF", "✍️ Paste Text"])
    
    resume_text = ""
    
    with tab1:
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        if uploaded_file != None:
            extracted = extract_text_from_pdf(uploaded_file)
            if extracted != None:
                st.success("PDF loaded successfully!")
                resume_text = extracted
                
                # Show text area preview
                with st.expander("Preview Extracted Text"):
                    resume_text = st.text_area("Verify text:", value=resume_text, height=200)
                    
    with tab2:
        resume_text_manual = st.text_area("Paste resume text here:", height=300)
        if resume_text_manual != "":
            resume_text = resume_text_manual

with col2:
    st.markdown("""
        <div class="glass-card">
            <div class="card-header">
                Job Description
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    job_desc = st.text_area("Paste target job posting here:", height=350)

# Analyze Button
st.write("")
analyze_button = st.button("🚀 Run Analysis")
st.write("")

# --- Show Results ---
if analyze_button:
    if resume_text == "":
        st.error("Please provide your resume first!")
    elif job_desc == "":
        st.error("Please provide the job description!")
    elif api_key_input == "":
        st.error("Please enter your Gemini API Key in the sidebar!")
    else:
        # Show simple loading spinner
        with st.spinner("Analyzing..."):
            report = analyze_resume_gemini(api_key_input, resume_text, job_desc)
        
        if report != None:
            st.markdown("""
                <div class="glass-card">
                    <div class="card-header">
                        ATS Match Results
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Split columns for Score and Feedback
            score_col, feedback_col = st.columns([1, 2])
            
            score = report.get("score", 0)
            rating = report.get("rating", "N/A")
            
            # Choose color based on score
            if score >= 80:
                color = "#10B981"
                bg_color = "rgba(16, 185, 129, 0.15)"
            elif score >= 60:
                color = "#F59E0B"
                bg_color = "rgba(245, 158, 11, 0.15)"
            else:
                color = "#EF4444"
                bg_color = "rgba(239, 68, 68, 0.15)"
            
            # Calculate SVG offset
            offset = 502.6 - (502.6 * (score / 100))
            
            with score_col:
                st.markdown(f"""
                    <div class="result-inner-card score-inner-card">
                        <h4 class="score-title">Match Score</h4>
                        <svg width="180" height="180" viewBox="0 0 200 200">
                            <circle cx="100" cy="100" r="80" class="svg-track" stroke-width="14" fill="transparent" />
                            <circle cx="100" cy="100" r="80" stroke="{color}" stroke-width="14" fill="transparent"
                                stroke-dasharray="502.6" stroke-dashoffset="{offset}" stroke-linecap="round"
                                style="transform: rotate(-90deg); transform-origin: 50% 50%;" />
                            <text x="100" y="105" text-anchor="middle" class="svg-text-main" font-size="44" font-weight="bold">{score}</text>
                            <text x="100" y="132" text-anchor="middle" class="svg-text-sub" font-size="14">/ 100</text>
                        </svg>
                        <div style="margin-top: 20px; padding: 8px 20px; border-radius: 30px; background-color: {bg_color}; color: {color}; font-weight: 700; font-size: 0.95rem;">
                            {rating}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            with feedback_col:
                st.markdown(f"""
                    <div class="result-inner-card feedback-inner-card">
                        <h4 style="margin: 0 0 15px 0; color: #8B5CF6; font-size: 1.1rem;">Recruiter Feedback Summary</h4>
                        <p style="font-size: 1.05rem; line-height: 1.6;">{report.get("feedback", "")}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            # Bottom Columns
            bot_col1, bot_col2 = st.columns(2)
            
            with bot_col1:
                # Keywords Card
                st.markdown("""
                    <div class="result-inner-card keywords-inner-card">
                        <h4 style="margin: 0 0 15px 0; color: #EF4444; font-size: 1.1rem;">Missing Keywords & Skills</h4>
                        <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                keywords = report.get("missing_keywords", [])
                if len(keywords) > 0:
                    badge_html = ""
                    for kw in keywords:
                        badge_html = badge_html + f'<span class="keyword-badge">{kw}</span>'
                    st.markdown(badge_html, unsafe_allow_html=True)
                else:
                    st.write("No missing keywords identified!")
                    
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Strengths Card
                st.markdown("""
                    <div class="result-inner-card">
                        <h4 style="margin: 0 0 15px 0; color: #10B981; font-size: 1.1rem;">Resume Strengths</h4>
                        <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                strengths = report.get("strengths", [])
                for s in strengths:
                    st.markdown(f"""
                        <div class="list-item">
                            <span class="list-icon text-success-custom">✔️</span>
                            <span>{s}</span>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)
                
            with bot_col2:
                # Suggestions Card
                st.markdown("""
                    <div class="result-inner-card suggestions-inner-card">
                        <h4 style="margin: 0 0 15px 0; color: #F59E0B; font-size: 1.1rem;">Recommendations to Improve Score</h4>
                        <div style="margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                suggestions = report.get("suggestions", [])
                for sugg in suggestions:
                    st.markdown(f"""
                        <div class="list-item">
                            <span class="list-icon text-warning-custom">💡</span>
                            <span>{sugg}</span>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)
