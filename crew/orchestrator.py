from shared.db import get_supabase


def run_pipeline():

    supabase = get_supabase()

    logs = []
    logs.append("Recruitment pipeline started")

    # Fetch all candidates
    response = supabase.table("candidates").select("*").execute()
    candidates = response.data

    if not candidates:
        logs.append("No candidates found")
        return logs

    for candidate in candidates:

        name = candidate.get("name")
        candidate_id = candidate.get("id")

        score = candidate.get("source_quality_score")

        # Handle None scores
        if score is None:
            score = 0

        logs.append(f"Processing candidate: {name} | Score: {score}")

        # Decision logic
        if score >= 7:

            supabase.table("candidates") \
                .update({"status": "shortlisted"}) \
                .eq("id", candidate_id) \
                .execute()

            logs.append(f"{name} → Shortlisted")

        else:

            supabase.table("candidates") \
                .update({"status": "rejected"}) \
                .eq("id", candidate_id) \
                .execute()

            logs.append(f"{name} → Rejected")

    logs.append("Recruitment pipeline finished")

    return logs


# ---------------------------------------------------
# Candidate Ranking System
# ---------------------------------------------------

def get_candidate_rankings():

    supabase = get_supabase()

    response = supabase.table("candidates").select("*").execute()
    candidates = response.data

    if not candidates:
        return []

    # Replace None scores
    for c in candidates:
        if c.get("source_quality_score") is None:
            c["source_quality_score"] = 0

    # Sort by score (highest first)
    ranked_candidates = sorted(
        candidates,
        key=lambda x: x["source_quality_score"],
        reverse=True
    )

    return ranked_candidates