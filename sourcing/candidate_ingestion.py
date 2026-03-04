"""
candidate_ingestion.py  –  Member 1 | Day 3
────────────────────────────────────────────
Inserts candidates into Supabase using ONLY the columns
that currently exist in Member 4's candidates table:

    id, name, email, phone, job_id, job_applied
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from shared.db import get_supabase

supabase = get_supabase()


def add_candidate(name: str, email: str, phone: str,
                  job_applied: str, job_id: int = None) -> dict:
    """
    Insert one candidate into the candidates table.
    Only uses columns that exist in Member 4's current table.
    """

    record = {
        "name":        name,
        "email":       email,
        "phone":       phone,
        "job_applied": job_applied,
    }

    # job_id is optional — only add if provided
    if job_id is not None:
        record["job_id"] = job_id

    result = supabase.table("candidates").insert(record).execute()
    print(f"✅ Candidate added → {name} | {email} | {job_applied}")
    return result.data[0] if result.data else {}


# ── Quick test ────────────────────────────────────────────────
if __name__ == "__main__":
    test = add_candidate(
        name        = "Test Candidate",
        email       = "test@example.com",
        phone       = "9999999999",
        job_applied = "Python Developer",
    )
    print("Inserted row:", test)
