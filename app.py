"""
app.py — TalentAI Recruitment System
Main entry point: streamlit run app.py
"""

import streamlit as st
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared.ui_theme import apply_theme


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="TalentAI Recruitment System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------

if "portal" not in st.session_state:
    st.session_state.portal = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# -------------------------------------------------
# PORTAL PAGES REGISTRATION
# -------------------------------------------------

def get_hr_pages():
    """Return HR portal page definitions."""
    return [
        st.Page("pages/hr_dashboard.py", title="HR Dashboard", icon="📊"),
        st.Page("pages/post_job.py", title="Post Job", icon="📝"),
        st.Page("pages/run_pipeline.py", title="Run Screening Pipeline", icon="⚙️"),
        st.Page("pages/candidate_database.py", title="Candidate Database", icon="👥"),
        st.Page("pages/screening_results.py", title="Screening Results", icon="📋"),
        st.Page("pages/scheduler_page.py", title="Interview Scheduler", icon="📅"),
        st.Page("pages/analytics_page.py", title="Analytics", icon="📈"),
    ]


def get_candidate_pages():
    """Return candidate portal page definitions."""
    return [
        st.Page("pages/apply_job.py", title="Apply for Job", icon="💼"),
        st.Page("pages/chatbot_page.py", title="AI Chatbot", icon="🤖"),
        st.Page("pages/scheduler_page.py", title="Interview Scheduler", icon="📅"),
    ]


# -------------------------------------------------
# LANDING PAGE
# -------------------------------------------------

def show_landing_page():
    """Show the main landing page with portal selection."""

    st.markdown("""
    <div style='text-align: center; padding: 3rem 0 1rem 0;'>
        <h1 style='font-size: 3rem !important; margin-bottom: 0.3rem !important;'>
            🧠 TalentAI
        </h1>
        <p style='color: #7878a0; font-size: 1.2rem; margin-top: 0;'>
            AI-Powered Recruitment Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    col1, col_spacer, col2 = st.columns([1, 0.3, 1])

    with col1:
        st.markdown("""
        <div class='portal-card'>
            <div class='icon'>👔</div>
            <h2>HR Portal</h2>
            <p>Manage jobs, screen candidates, schedule interviews & view analytics</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter HR Portal", key="hr_btn", use_container_width=True):
            st.session_state.portal = "hr"
            st.rerun()

    with col2:
        st.markdown("""
        <div class='portal-card'>
            <div class='icon'>🎯</div>
            <h2>Candidate Portal</h2>
            <p>Apply for jobs, chat with AI assistant & schedule interviews</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Candidate Portal", key="cand_btn", use_container_width=True):
            st.session_state.portal = "candidate"
            st.rerun()

    st.markdown("""
    <div style='text-align: center; margin-top: 4rem; color: #3a3a5c; font-size: 0.85rem;'>
        Powered by Groq LLM · ChromaDB · Supabase
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# HR LOGIN
# -------------------------------------------------

def show_hr_login():
    """Show HR login form."""

    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h1 style='font-size: 2rem !important;'>🔐 HR Portal Login</h1>
        <p style='color: #7878a0;'>Enter your credentials to access the HR dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        with st.form("hr_login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if username == "admin" and password == "talentai123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

        if st.button("← Back to Home", use_container_width=True):
            st.session_state.portal = None
            st.query_params.clear()
            st.rerun()


# -------------------------------------------------
# MAIN ROUTING
# -------------------------------------------------

portal = st.session_state.portal

if portal == "hr" and st.session_state.authenticated:
    # Show HR navigation
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='font-size: 1.3rem !important; margin: 0 !important;'>🧠 TalentAI</h2>
            <p style='color: #7878a0; font-size: 0.8rem; margin: 0;'>HR Portal</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    nav = st.navigation(get_hr_pages())

    with st.sidebar:
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.portal = None
            st.query_params.clear()
            st.rerun()

    nav.run()

elif portal == "candidate":
    # Show Candidate navigation
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='font-size: 1.3rem !important; margin: 0 !important;'>🧠 TalentAI</h2>
            <p style='color: #7878a0; font-size: 0.8rem; margin: 0;'>Candidate Portal</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    nav = st.navigation(get_candidate_pages())

    with st.sidebar:
        st.divider()
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.portal = None
            st.query_params.clear()
            st.rerun()

    nav.run()

elif portal == "hr" and not st.session_state.authenticated:
    # HR login — use st.navigation to suppress auto-discovered pages
    nav = st.navigation([st.Page(show_hr_login, title="HR Login", icon="🔐")])
    nav.run()

else:
    # Landing page — use st.navigation to suppress auto-discovered pages
    nav = st.navigation([st.Page(show_landing_page, title="TalentAI", icon="🧠")])
    nav.run()
