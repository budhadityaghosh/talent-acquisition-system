"""
bias_filter.py  –  Member 1 | Day 6
──────────────────────────────────────
Anonymizes candidate name in Supabase for fair hiring.
Works with Member 4's actual table columns:
    id, name, email, phone, job_id, job_applied

Since resume_text column doesn't exist yet, we anonymize
only the name field (the only PII we can act on right now).

Run from project ROOT:
    python sourcing/bias_filter.py
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from shared.db import get_supabase
from dotenv import load_dotenv

load_dotenv()
supabase = get_supabase()


def anonymize_name(candidate_id: int) -> None:
    """Replace a candidate's real name with an anonymous ID."""
    supabase.table("candidates").update({
        "name": f"Candidate_{candidate_id}"
    }).eq("id", candidate_id).execute()


def apply_bias_filter(job_id: int) -> str:
    """
    Anonymize all candidates for a given job_id.
    Replaces their real name with Candidate_<id>.
    """

    print(f"\n{'='*55}")
    print(f"  BIAS FILTER — JOB ID: {job_id}")
    print(f"{'='*55}\n")

    result = supabase.table("candidates") \
        .select("id, name") \
        .eq("job_id", job_id) \
        .execute()

    candidates = result.data

    if not candidates:
        msg = f"No candidates found for Job ID {job_id}."
        print(msg)
        return msg

    print(f"Found {len(candidates)} candidates to anonymize...\n")

    for c in candidates:
        anonymize_name(c["id"])
        print(f"  ✅ {c['name']} → Candidate_{c['id']}")

    summary = f"\n✅ Bias filter complete — {len(candidates)} names anonymized."
    print(summary)
    print("\nScreening module will now evaluate candidates on skills only.")
    return summary


if __name__ == "__main__":
    try:
        job_id = int(input("Enter Job ID to apply bias filter: ").strip())
        apply_bias_filter(job_id)
    except ValueError:
        print("❌ Enter a valid number.")
    except KeyboardInterrupt:
        print("\nCancelled.")
