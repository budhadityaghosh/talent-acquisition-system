import plotly.express as px
import streamlit as st
from datetime import datetime, date
import sys
import os

# allow imports from shared folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared.db import get_supabase
from shared.chroma_setup import get_chroma

supabase = get_supabase()
chroma_collection = get_chroma()

st.set_page_config(page_title="HR Manager Dashboard", layout="wide")

st.title("🧑‍💼 HR Manager Dashboard")
# ===============================
# DASHBOARD ANALYTICS
# ===============================

st.subheader("📊 Recruitment Overview")

try:
    jobs = supabase.table("jobs").select("*").execute().data
    candidates = supabase.table("candidates").select("*").execute().data
    slots = supabase.table("interview_slots").select("*").execute().data

    total_jobs = len(jobs)
    total_candidates = len(candidates)

    scheduled_interviews = len([s for s in slots if s.get("is_booked") == True])
    open_slots = len([s for s in slots if s.get("is_booked") == False])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Jobs", total_jobs)
    col2.metric("Candidates", total_candidates)
    col3.metric("Scheduled Interviews", scheduled_interviews)
    col4.metric("Open Slots", open_slots)

except:
    st.info("Analytics will appear once data is available.")

    # ===============================
# HIRING FUNNEL VISUALIZATION
# ===============================

st.subheader("📈 Hiring Pipeline")

try:

    candidates = supabase.table("candidates").select("*").execute().data
    slots = supabase.table("interview_slots").select("*").execute().data

    total_candidates = len(candidates)

    screened = len([c for c in candidates if c.get("resume_text")])
    shortlisted = len([c for c in candidates if c.get("source_quality_score",0) >= 7])
    interviews = len([s for s in slots if s.get("is_booked") == True])

    funnel_data = {
        "Stage": [
            "Candidates",
            "Screened",
            "Shortlisted",
            "Interview"
        ],
        "Count": [
            total_candidates,
            screened,
            shortlisted,
            interviews
        ]
    }

    fig = px.funnel(
        funnel_data,
        x="Count",
        y="Stage"
    )

    st.plotly_chart(fig, use_container_width=True)

except:
    st.info("Pipeline analytics will appear once candidate data is available.")

tabs = st.tabs([
    "Post New Job",
    "All Candidates",
    "Scheduled Interviews",
    "Add Interview Slots"
])

# ===============================
# POST JOB TAB
# ===============================

with tabs[0]:

    st.header("Post a New Job")

    with st.form("job_form"):

        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company Name *")
            job_title = st.text_input("Job Title *")

            experience_years = st.selectbox(
                "Experience Required",
                ["0-1 years", "1-3 years", "3-5 years", "5+ years"]
            )

            location = st.text_input("Location")
            salary_range = st.text_input("Salary Range")

        with col2:
            education = st.text_input("Education Requirement")
            skills_required = st.text_area("Required Skills *")
            dealbreakers = st.text_area("Dealbreakers")
            requirements = st.text_area("Detailed Job Description *")

        submit = st.form_submit_button("Post Job")

    if submit:

        if company_name.strip() == "" or job_title.strip() == "" or requirements.strip() == "":
            st.error("Please fill all required fields.")
        else:

            job_data = {
                "job_title": job_title,
                "company_name": company_name,
                "requirements": requirements,
                "skills_required": skills_required,
                "experience_years": experience_years,
                "education": education,
                "location": location,
                "salary_range": salary_range,
                "dealbreakers": dealbreakers,
                "created_at": datetime.now().isoformat()
            }

            try:

                supabase.table("jobs").insert(job_data).execute()

                # store job context in vector DB
                full_job_text = f"""
                Company: {company_name}
                Job Title: {job_title}
                Requirements: {requirements}
                Skills Required: {skills_required}
                Experience: {experience_years}
                """

                chroma_collection.add(
                    documents=[full_job_text],
                    ids=[f"{company_name}_{job_title}_{datetime.now().timestamp()}"]
                )

                st.success("Job posted successfully!")

            except Exception as e:
                st.error("Error posting job")
                st.write(e)

# ===============================
# CANDIDATES TAB
# ===============================

with tabs[1]:

    st.header("All Candidates")

    try:

        result = supabase.table("candidates").select("*").execute()

        candidates = result.data

        if not candidates:
            st.info("No candidates available yet.")
        else:

            for c in candidates:

                with st.container():

                    col1, col2 = st.columns([2,1])

                    with col1:
                        st.subheader(c.get("name","Unknown"))
                        st.write("📧", c.get("email",""))
                        st.write("📞", c.get("phone",""))
                        st.write("Job Applied:", c.get("job_applied",""))

                    with col2:
                        st.metric("Source Score", c.get("source_quality_score",0))

                    st.divider()

    except Exception as e:
        st.error("Error loading candidates")
        st.write(e)

# ===============================
# INTERVIEW SCHEDULE TAB
# ===============================

with tabs[2]:

    st.header("Scheduled Interviews")

    try:

        result = supabase.table("interview_slots").select("*").execute()

        slots = result.data

        booked_slots = [s for s in slots if s.get("is_booked") == True]

        if not booked_slots:
            st.info("No interviews scheduled yet.")
        else:

            for s in booked_slots:

                st.write("Candidate:", s.get("candidate_name",""))
                st.write("Interviewer:", s.get("interviewer_name",""))
                st.write("Date:", s.get("date",""))
                st.write("Time:", s.get("time",""))

                st.divider()

    except Exception as e:
        st.error("Error loading interviews")
        st.write(e)

# ===============================
# ADD INTERVIEW SLOT TAB
# ===============================

with tabs[3]:

    st.header("Add Interview Slots")

    with st.form("slot_form"):

        interviewer_name = st.text_input("Interviewer Name")

        interview_date = st.date_input("Interview Date", min_value=date.today())

        times = st.multiselect(
            "Select Time Slots",
            [
                "10:00 AM",
                "11:00 AM",
                "12:00 PM",
                "2:00 PM",
                "3:00 PM",
                "4:00 PM"
            ]
        )

        submit_slots = st.form_submit_button("Add Slots")

    if submit_slots:

        try:

            for time in times:

                slot_data = {
                    "date": str(interview_date),
                    "time": time,
                    "is_booked": False,
                    "candidate_id": None,
                    "candidate_name": None,
                    "interviewer_name": interviewer_name,
                    "created_at": datetime.now().isoformat()
                }

                supabase.table("interview_slots").insert(slot_data).execute()

            st.success("Interview slots added!")

        except Exception as e:
            st.error("Error adding slots")
            st.write(e)