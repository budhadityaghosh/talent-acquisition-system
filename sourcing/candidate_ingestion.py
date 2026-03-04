"""
candidate_ingestion.py  -  Member 1 | Day 3
Uses all columns now available in Member 4's candidates table:
id, name, email, phone, job_id, job_applied,
resume_text, source_quality_score, screening_score, status
"""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def add_candidate(name: str, email: str, phone: str,
                  job_applied: str, job_id: int = None,
                  resume_text: str = "", status: str = "applied",
                  source_quality_score: int = 0) -> dict:
    """Insert one candidate into Supabase candidates table."""

    record = {
        "name":                 name,
        "email":                email,
        "phone":                phone,
        "job_applied":          job_applied,
        "resume_text":          resume_text[:5000],
        "status":               status,
        "source_quality_score": source_quality_score,
    }
    if job_id is not None:
        record["job_id"] = job_id

    result = supabase.table("candidates").insert(record).execute()
    print(f"✅ Inserted: {name} | {email} | status={status} | score={source_quality_score}")
    return result.data[0] if result.data else {}


# ── Quick test ────────────────────────────────────────────────
if __name__ == "__main__":
    add_candidate(
        name                 = "Test Candidate",
        email                = "test2@example.com",
        phone                = "9999999999",
        job_applied          = "AI Engineer",
        job_id               = 4,
        resume_text          = "Python developer, 2 years experience, SQL, Django.",
        status               = "applied",
        source_quality_score = 0,
    )
    print("Check Supabase → candidates table.")