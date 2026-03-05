import sys
import os
import json
from google import genai
from dotenv import load_dotenv

# allow importing shared modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from shared.db import get_supabase
from shared.chroma_setup import get_job_context, get_candidates_collection

load_dotenv()

# configure Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Supabase connection
supabase = get_supabase()


def screen_one_candidate(resume_text, job_context):

    prompt = f"""
You are a senior HR screener. Score this candidate ONLY against the company
requirements below. Do not use generic opinions.

COMPANY REQUIREMENTS (from ChromaDB — RAG):
{job_context}

CANDIDATE RESUME:
{resume_text}

Return ONLY valid JSON — no markdown:

{{
"screening_score": <0-100>,
"skills_matched": ["skill1", "skill2"],
"skills_missing": ["skill3", "skill4"],
"experience_fit": "<good|average|poor>",
"culture_fit": "<good|average|poor>",
"recommendation": "<shortlist|reject|maybe>",
"summary": "<two sentences>"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # clean Gemini formatting
    if "```" in raw:
        raw = raw.split("```")[1]

    if raw.startswith("json"):
        raw = raw[4:]

    raw = raw.strip()

    try:
        return json.loads(raw)

    except json.JSONDecodeError:

        print("⚠ Gemini returned invalid JSON. Using fallback result.")

        return {
            "screening_score": 50,
            "skills_matched": [],
            "skills_missing": [],
            "experience_fit": "average",
            "culture_fit": "average",
            "recommendation": "maybe",
            "summary": "Fallback result due to parsing error."
        }


def run_screening(job_id):

    job_context = get_job_context(job_id)

    if not job_context:
        print(f"Job {job_id} not found in ChromaDB.")
        return "Failed"

    result = (
        supabase.table("candidates")
        .select("*")
        .eq("job_id", job_id)
        .in_("status", ["applied", "sourced_qualified"])
        .execute()
    )

    candidates = result.data

    print(f"\nScreening {len(candidates)} candidates for job {job_id}")
    print("=" * 55)

    shortlisted = 0
    rejected = 0
    maybe = 0

    for c in candidates:

        print(f"Screening: {c['name']}...")

        try:

            score = screen_one_candidate(c["resume_text"], job_context)

            status_map = {
                "shortlist": "shortlisted",
                "reject": "rejected",
                "maybe": "maybe"
            }

            new_status = status_map.get(score["recommendation"], "maybe")
            if new_status == "shortlisted":
                try:
                    from engagement.telegram_notifier import send_shortlist_notification

                    send_shortlist_notification(
                        candidate_name=c["name"],
                        chat_id=c.get("telegram_chat_id"),
                        job_title=c.get("job_applied", "")
                    )

                except Exception as e:
                    print("Telegram shortlist notification failed:", e)

            # update database
            supabase.table("candidates").update({

                "screening_score": score["screening_score"],
                "skills_matched": ", ".join(score.get("skills_matched", [])),
                "skills_missing": ", ".join(score.get("skills_missing", [])),
                "culture_fit": score.get("culture_fit", ""),
                "recommendation": score.get("recommendation", ""),
                "status": new_status

            }).eq("id", c["id"]).execute()

            # store in ChromaDB
            coll = get_candidates_collection()

            coll.upsert(
                documents=[f"Score:{score['screening_score']} {c['resume_text'][:300]}"],
                ids=[str(c["id"])]
            )

            print(f"✓ {score['screening_score']}/100 → {new_status.upper()}")

            if new_status == "shortlisted":
                shortlisted += 1
            elif new_status == "rejected":
                rejected += 1
            else:
                maybe += 1

        except Exception as e:

            print(f"Error: {e}")

            supabase.table("candidates").update(
                {"status": "maybe"}
            ).eq("id", c["id"]).execute()

    summary = f"Done. Shortlisted: {shortlisted} | Maybe: {maybe} | Rejected: {rejected}"

    print(f"\n{summary}")

    return summary


if __name__ == "__main__":

    job_id = int(input("Enter Job ID: "))

    run_screening(job_id)