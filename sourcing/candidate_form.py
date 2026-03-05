"""
candidate_form.py  -  Member 1 | Day 3 (updated for new columns)
Run: streamlit run sourcing/candidate_form.py
"""

import streamlit as st
import io
import os
import PyPDF2
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── PDF text extractor ────────────────────────────────────────
def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text.strip() if text.strip() else "Could not extract text from PDF."
    except Exception as e:
        return f"PDF error: {e}"

# ── Page config ───────────────────────────────────────────────
st.set_page_config(page_title="Apply Now | TalentAI", page_icon="💼", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; background:#0a0a0f; color:#e8e8f0; }
#MainMenu, footer, header { visibility:hidden; }
.main .block-container { background:#0a0a0f; padding:2.5rem 2rem; max-width:720px; }
h1,h2,h3 { font-family:'Syne',sans-serif !important; font-weight:800 !important; color:#ffffff !important; }
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div {
    background:#13131f !important; border:1px solid #2a2a3e !important;
    border-radius:10px !important; color:#e8e8f0 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color:#6c63ff !important; box-shadow:0 0 0 3px rgba(108,99,255,0.15) !important;
}
label { color:#c0c0d8 !important; font-size:0.875rem !important; font-weight:500 !important; }
[data-testid="stFileUploader"] {
    background:#13131f !important; border:1px dashed #3a3a5a !important; border-radius:10px !important;
}
[data-testid="stFormSubmitButton"] > button {
    background:linear-gradient(135deg,#6c63ff 0%,#a855f7 100%) !important;
    color:white !important; width:100% !important; border-radius:10px !important;
    padding:0.8rem !important; font-size:1rem !important; font-weight:600 !important;
    border:none !important; box-shadow:0 4px 20px rgba(108,99,255,0.35) !important;
}
.stAlert { border-radius:10px !important; border:none !important; }
hr { border-color:#1e1e2e !important; margin:1.5rem 0 !important; }
.sec { font-size:0.7rem; font-weight:600; color:#6c63ff;
       text-transform:uppercase; letter-spacing:0.12em; margin:1.5rem 0 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; padding:1.5rem 0 1rem 0;'>
  <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:#fff;'>
    💼 Apply Now
  </div>
  <p style='color:#7878a0; font-size:0.88rem; margin-top:0.4rem;'>
    Submit your application — our AI reviews it within minutes
  </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Load jobs ─────────────────────────────────────────────────
try:
    jobs = supabase.table("jobs").select("id, job_title, company_name").execute().data
except Exception as e:
    st.error(f"Cannot connect to database: {e}")
    st.stop()

if not jobs:
    st.warning("No open positions right now.")
    st.stop()

job_options = {f"{j['job_title']} at {j['company_name']}": j["id"] for j in jobs}

# ── Form ──────────────────────────────────────────────────────
with st.form("apply_form"):

    st.markdown('<div class="sec">👤 Personal Details</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name  = st.text_input("Full Name *",    placeholder="e.g. Rahul Sharma")
        phone = st.text_input("Phone Number *", placeholder="e.g. 9876543210")
    with col2:
        email      = st.text_input("Email Address *", placeholder="e.g. rahul@gmail.com")
        experience = st.selectbox("Years of Experience",
                                  ["0-1 years","1-3 years","3-5 years","5-10 years","10+ years"])

    st.markdown('<div class="sec">💼 Position</div>', unsafe_allow_html=True)
    selected_label = st.selectbox("Position Applying For *", list(job_options.keys()))

    st.markdown('<div class="sec">📄 Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume PDF *", type=["pdf"])
    cover_note  = st.text_area("Cover Note (Optional)", height=80,
                               placeholder="Why are you a great fit?")

    submitted = st.form_submit_button("🚀 Submit My Application", use_container_width=True)

# ── Handle submission ─────────────────────────────────────────
if submitted:
    if not name.strip() or not email.strip() or not phone.strip() or not resume_file:
        st.error("Please fill in all required fields marked with *")
    else:
        with st.spinner("Submitting..."):
            try:
                # Extract resume text from PDF
                pdf_bytes   = resume_file.read()
                resume_text = extract_pdf_text(pdf_bytes)

                # Build full resume block
                full_resume = (
                    f"Experience: {experience}\n"
                    f"Cover Note: {cover_note.strip()}\n\n"
                    f"--- RESUME ---\n{resume_text}"
                )

                supabase.table("candidates").insert({
                    "name":                 name.strip(),
                    "email":                email.strip().lower(),
                    "phone":                phone.strip(),
                    "job_id":               job_options[selected_label],
                    "job_applied":          selected_label,
                    "resume_text":          full_resume[:5000],
                    "status":               "applied",
                    "source_quality_score": 0,
                }).execute()

                st.success("✅ Application submitted successfully!")
                st.balloons()
                st.markdown(f"""
                <div style='background:#0d2b1a; border:1px solid #166534;
                            border-radius:12px; padding:1.2rem 1.5rem; margin-top:1rem;'>
                  <div style='color:#4ade80; font-size:0.75rem;
                              text-transform:uppercase; margin-bottom:0.4rem;'>
                    Application Received ✓
                  </div>
                  <div style='color:#fff; font-size:1rem; font-weight:600;'>{name.strip()}</div>
                  <div style='color:#7878a0; font-size:0.85rem; margin-top:0.3rem;'>{selected_label}</div>
                  <div style='color:#4a4a6a; font-size:0.78rem; margin-top:0.5rem;'>
                    Resume extracted and saved. Our AI will screen your profile shortly.
                  </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Database error: {e}")