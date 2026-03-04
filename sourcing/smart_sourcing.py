"""
smart_sourcing.py  –  Member 1 | Days 4–5
──────────────────────────────────────────
Auto-fetches 15 simulated candidate profiles, scores each with Gemini AI
against the job requirements in ChromaDB, and inserts them into Supabase.

Only inserts columns that exist in Member 4's candidates table:
    name, email, phone, job_id, job_applied

Run from project ROOT:
    python sourcing/smart_sourcing.py
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests
import json
from datetime import datetime

from shared.db import get_supabase
from shared.chroma_setup import get_job_context
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model   = genai.GenerativeModel("gemini-1.5-flash")
supabase = get_supabase()


def fetch_profiles(count=15):
    """Fetch simulated Indian candidate profiles from randomuser.me (free, no key needed)."""
    try:
        r = requests.get(f"https://randomuser.me/api/?results={count}&nat=in", timeout=10)
        r.raise_for_status()
        print(f"✅ Fetched {count} profiles from randomuser.me")
        return r.json()["results"]
    except Exception as e:
        print(f"❌ Fetch failed: {e}")
        return []


def build_profile_text(p):
    """Turn a randomuser.me profile dict into readable text for AI scoring."""
    age = p['dob']['age']
    if age < 25:   skills = "Python basics, SQL, College projects, Excel"
    elif age < 30: skills = "Python, SQL, Pandas, REST APIs, Git, 2 years exp"
    elif age < 40: skills = "Python, SQL, Pandas, Power BI, Team lead, 5 years exp"
    else:          skills = "Python, SQL, Data Warehousing, Management, 10+ years exp"

    return (
        f"Name: {p['name']['first']} {p['name']['last']}\n"
        f"Location: {p['location']['city']}, {p['location']['state']}\n"
        f"Age: {age}\n"
        f"Email: {p['email']}\n"
        f"Simulated Skills: {skills}\n"
    )


def score_with_ai(profile_text, job_context):
    """Ask Gemini to score the candidate against job requirements. Returns dict."""
    prompt = f"""
You are a talent sourcing assistant.

JOB REQUIREMENTS (from company database):
{job_context}

CANDIDATE PROFILE:
{profile_text}

Return ONLY valid JSON, no markdown:
{{
    "source_quality_score": <0-100>,
    "should_proceed": <true if score >= 50>,
    "reason": "<one sentence>"
}}
"""
    try:
        raw = model.generate_content(prompt).text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"  ⚠️  AI scoring error: {e} — defaulting to 50")
        return {"source_quality_score": 50, "should_proceed": True, "reason": "Parse error"}


def run_sourcing(job_id: int):
    """Full sourcing pipeline for a given job ID."""

    print(f"\n{'='*60}")
    print(f"  SMART SOURCING — JOB ID: {job_id}")
    print(f"{'='*60}\n")

    # Get job requirements from ChromaDB
    job_context = get_job_context(job_id)
    if not job_context:
        print(f"❌ Job {job_id} not found in ChromaDB.")
        print("   Ask Member 4 to re-post the job through the HR portal.")
        return

    # Get job title + company from Supabase
    job_row = supabase.table("jobs").select("job_title, company_name").eq("id", job_id).execute()
    if not job_row.data:
        print(f"❌ Job {job_id} not found in Supabase jobs table.")
        return

    job_title = job_row.data[0]["job_title"]
    company   = job_row.data[0]["company_name"]
    job_label = f"{job_title} at {company}"

    print(f"📋 Sourcing for: {job_label}\n")

    profiles = fetch_profiles(15)
    if not profiles:
        return

    passed = filtered = 0

    print(f"  {'Name':<16} {'Score':>6}   {'Decision'}")
    print(f"  {'-'*45}")

    for p in profiles:
        profile_text = build_profile_text(p)
        result       = score_with_ai(profile_text, job_context)
        name         = f"{p['name']['first']} {p['name']['last']}"

        # ── Only insert columns that EXIST in Member 4's table ──
        supabase.table("candidates").insert({
            "name":        name,
            "email":       p["email"],
            "phone":       p["phone"],
            "job_id":      job_id,
            "job_applied": job_label,
        }).execute()

        icon   = "✅" if result["should_proceed"] else "❌"
        label  = "QUALIFIED" if result["should_proceed"] else "FILTERED"
        print(f"  {icon} {name:<16} {result['source_quality_score']:>3}/100  {label}")

        if result["should_proceed"]: passed  += 1
        else:                        filtered += 1

    print(f"\n{'='*60}")
    print(f"  SOURCING COMPLETE")
    print(f"  ✅ Qualified : {passed}")
    print(f"  ❌ Filtered  : {filtered}")
    print(f"{'='*60}")
    print(f"\nCheck Member 4's dashboard → Candidate Pipeline tab.")


if __name__ == "__main__":
    try:
        job_id = int(input("Enter Job ID (from Member 4's HR portal): ").strip())
        run_sourcing(job_id)
    except ValueError:
        print("❌ Please enter a valid number.")
    except KeyboardInterrupt:
        print("\nCancelled.")
