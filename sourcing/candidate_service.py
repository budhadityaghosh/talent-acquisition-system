"""
candidate_service.py  -  Member 1 | Day 3
Combines resume parsing + DB insertion. Uses all available columns.
"""

import os
import sys
import io
import PyPDF2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sourcing.candidate_ingestion import add_candidate


def extract_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = "".join(p.extract_text() or "" for p in reader.pages)
        return text.strip() or "Could not extract text."
    except Exception as e:
        return f"PDF error: {e}"


def ingest_from_upload(name, email, phone, job_applied, pdf_bytes,
                       job_id=None, experience="", cover_note=""):
    """Parse PDF bytes and insert candidate — used by candidate_form.py."""
    resume_text = extract_pdf(pdf_bytes)
    full = f"Experience: {experience}\nCover Note: {cover_note}\n\n--- RESUME ---\n{resume_text}"
    return add_candidate(name, email, phone, job_applied, job_id,
                         resume_text=full, status="applied")


# ── Quick test ────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("Arjun Mehta",  "arjun@test.com",  "9876500001", "AI Engineer", 4,
         "3 years Python, SQL, Pandas. B.Tech CS."),
        ("Sneha Patel",  "sneha@test.com",  "9876500002", "AI Engineer", 4,
         "2 years Python, Power BI. MBA Finance."),
        ("Ravi Kumar",   "ravi@test.com",   "9876500003", "AI Engineer", 4,
         "Fresher. Basic Python. No work experience."),
    ]
    for name, email, phone, job, jid, resume in tests:
        add_candidate(name, email, phone, job, jid,
                      resume_text=resume, status="applied", source_quality_score=0)
    print("\n✅ 3 test candidates inserted. Check Supabase.")