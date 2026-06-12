from agents.matcher_agent import run_matcher


def matcher_node(state):

    matched, partial, missing = run_matcher(
        state["resume_skills"],
        state["jd_skills"]
    )

    coverage = 0

    if state["jd_skills"]:
        coverage = int(
            len(matched) / len(state["jd_skills"]) * 100
        )

    return {
        "matched": list(matched),
        "partial": list(partial),
        "missing": list(missing),
        "coverage": coverage
    }