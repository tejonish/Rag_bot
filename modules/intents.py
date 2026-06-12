def detect_intent(query):

    query = query.lower()

    if any(x in query for x in ["score", "fit"]):
        return "FIT_SCORE"

    elif any(x in query for x in ["missing", "lack", "skill"]):
        return "MISSING_SKILLS"

    elif any(x in query for x in ["roadmap", "learn", "improve"]):
        return "ROADMAP"

    elif any(x in query for x in ["resume", "summary", "summarize"]):
        return "RESUME_SUMMARY"

    elif any(x in query for x in ["interview", "prepare"]):
        return "INTERVIEW_HELP"

    return "GENERAL"