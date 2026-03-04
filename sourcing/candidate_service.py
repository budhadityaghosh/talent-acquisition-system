"""
candidate_service.py  –  Member 1 | Day 3
──────────────────────────────────────────
Combines resume parsing + DB insertion into one call.
Only uses columns that exist in Member 4's candidates table.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sourcing.candidate_ingestion import add_candidate
from sourcing.resume_parser import parse_resume_pdf, parse_resume_file, clean_resume_text


def ingest_from_upload(name, email, phone, job_applied, pdf_bytes, job_id=None):
    """
    Used by candidate_form.py (Streamlit upload).
    Parses the PDF bytes and inserts the candidate.
    """
    raw   = parse_resume_pdf(pdf_bytes)
    clean = clean_resume_text(raw)
    print(f"📄 Resume extracted ({len(clean)} chars)")
    return add_candidate(name, email, phone, job_applied, job_id)


def ingest_from_file(name, email, phone, job_applied, file_path, job_id=None):
    """
    Used for testing — reads resume from a file path on disk.
    """
    raw   = parse_resume_file(file_path)
    clean = clean_resume_text(raw)
    print(f"📄 Resume extracted ({len(clean)} chars)")
    return add_candidate(name, email, phone, job_applied, job_id)


# ── Quick test: insert 3 dummy candidates ─────────────────────
if __name__ == "__main__":
    print("Inserting 3 test candidates...\n")
    tests = [
        ("Arjun Mehta",  "arjun@test.com",  "9876500001", "Python Data Analyst"),
        ("Sneha Patel",  "sneha@test.com",  "9876500002", "Python Data Analyst"),
        ("Ravi Kumar",   "ravi@test.com",   "9876500003", "Python Data Analyst"),
    ]
    for name, email, phone, job in tests:
        add_candidate(name, email, phone, job)
    print("\n✅ Done. Check Supabase → candidates table.")
