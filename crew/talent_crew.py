"""
talent_crew.py  –  Member 1 | Days 7–11
─────────────────────────────────────────
CrewAI pipeline that orchestrates 3 AI agents sequentially:

  Agent 1 (Sourcing)   → finds and scores candidates
  Agent 2 (Screening)  → reads resumes and ranks them
  Agent 3 (Engagement) → prepares shortlisted candidate report

All agents use Google Gemini 1.5 Flash (free tier).
Job requirements are retrieved from ChromaDB (RAG).

Run:  python talent_crew.py
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

# CrewAI internally tries to use OpenAI — set a placeholder to avoid errors
# We override it with Gemini via the LLM object below
os.environ["OPENAI_API_KEY"] = "placeholder-not-used"

# ── Gemini LLM config for CrewAI ─────────────────────────────
gemini_llm = LLM(
    model   = "gemini/gemini-1.5-flash",
    api_key = os.getenv("GEMINI_API_KEY")
)


def build_and_run_crew(job_id: int):
    """
    Build and execute the full 3-agent CrewAI talent pipeline for a given job.

    Parameters
    ----------
    job_id : The job ID from the Supabase jobs table
             (Member 4 posts the job → you get this ID)

    Returns
    -------
    CrewAI result object (printed to terminal)
    """

    print(f"\n{'='*60}")
    print(f"  CREWAI TALENT PIPELINE STARTING")
    print(f"  Job ID: {job_id}")
    print(f"{'='*60}\n")

    # ── AGENT 1: Sourcing Specialist ─────────────────────────
    sourcing_agent = Agent(
        role      = "Talent Sourcing Specialist",
        goal      = (
            "Source and quality-filter candidate profiles for the job. "
            "Only pass forward candidates who genuinely match requirements."
        ),
        backstory  = (
            "You are an expert talent sourcer with 8 years of experience "
            "finding great candidates from external platforms. You retrieve "
            "job requirements from the company knowledge base (ChromaDB) and "
            "evaluate each candidate profile strictly against them. "
            "You do not guess — you only proceed with evidence-based matches."
        ),
        llm     = gemini_llm,
        verbose = True
    )

    # ── AGENT 2: Resume Screening Expert ─────────────────────
    screening_agent = Agent(
        role      = "Resume Screening Expert",
        goal      = (
            "Score and rank all candidates using the company's specific "
            "requirements. Produce fair, grounded scores for every candidate."
        ),
        backstory  = (
            "You are a senior HR professional with deep expertise in matching "
            "candidates to technical roles. You read resumes carefully and "
            "compare each one to the company requirements retrieved from the "
            "vector database. You never give generic scores — every score is "
            "justified by specific skill matches and gaps."
        ),
        llm     = gemini_llm,
        verbose = True
    )

    # ── AGENT 3: Engagement Coordinator ──────────────────────
    engagement_agent = Agent(
        role      = "Candidate Engagement Coordinator",
        goal      = (
            "Prepare a clear, actionable engagement report for "
            "all shortlisted candidates."
        ),
        backstory  = (
            "You are an HR coordinator who ensures shortlisted candidates "
            "know their status and next steps. You produce clean, professional "
            "reports for the HR team showing exactly who is ready for interviews "
            "and what their scores mean."
        ),
        llm     = gemini_llm,
        verbose = True
    )

    # ── TASK 1: Sourcing ─────────────────────────────────────
    sourcing_task = Task(
        description    = (
            f"Source candidates for Job ID {job_id}. "
            f"Retrieve the job requirements from the ChromaDB knowledge base. "
            f"Fetch 15 candidate profiles from the external talent database. "
            f"Score each profile against the job requirements using AI analysis. "
            f"Insert all candidates into the system database with their scores "
            f"and status (sourced_qualified or sourced_filtered). "
            f"Return a clear summary: total fetched, total qualified, total filtered."
        ),
        expected_output = (
            "A summary showing: total profiles fetched, how many passed the "
            "quality filter (score ≥ 50), and how many were filtered out."
        ),
        agent = sourcing_agent
    )

    # ── TASK 2: Screening ────────────────────────────────────
    screening_task = Task(
        description    = (
            f"Screen all sourced candidates for Job ID {job_id}. "
            f"For each candidate with status 'sourced_qualified' or 'applied', "
            f"retrieve the company job requirements from ChromaDB. "
            f"Score the resume against those requirements (0–100). "
            f"Identify skills matched and skills missing. "
            f"Set status to: shortlisted (score ≥ 70), maybe (40–69), or rejected (<40). "
            f"Update all candidate records in the database. "
            f"Return a screening summary with counts."
        ),
        expected_output = (
            "A summary showing: total candidates screened, shortlisted count, "
            "maybe count, rejected count, and average score."
        ),
        agent = screening_agent
    )

    # ── TASK 3: Engagement Report ────────────────────────────
    engagement_task = Task(
        description    = (
            f"Review all shortlisted candidates for Job ID {job_id} in the database. "
            f"Prepare a structured engagement report listing each shortlisted candidate's "
            f"name, email, screening score, matched skills, and recommended next step. "
            f"Format it clearly so the HR team can immediately act on it."
        ),
        expected_output = (
            "A formatted list of all shortlisted candidates with: "
            "name, email, score out of 100, top matched skills, "
            "and recommended next step (e.g. send interview invite)."
        ),
        agent = engagement_agent
    )

    # ── ASSEMBLE AND RUN THE CREW ────────────────────────────
    crew = Crew(
        agents  = [sourcing_agent, screening_agent, engagement_agent],
        tasks   = [sourcing_task, screening_task, engagement_task],
        process = Process.sequential,   # agents run one after another
        verbose = True
    )

    print("🚀 Launching CrewAI pipeline...\n")
    result = crew.kickoff()

    print(f"\n{'='*60}")
    print("  ✅ PIPELINE COMPLETE")
    print(f"{'='*60}\n")
    print(result)

    return result


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    try:
        job_id = int(input("Enter Job ID to run the full CrewAI pipeline: ").strip())
        build_and_run_crew(job_id)
    except ValueError:
        print("❌ Enter a valid number for Job ID.")
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        print("\n📌 Common fixes:")
        print("  pip install litellm --upgrade")
        print("  pip install crewai --upgrade")
        print("  Check your GEMINI_API_KEY in .env")
