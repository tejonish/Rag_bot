from agents.scorer_agent import run_scorer


def scorer_node(state):

    score = run_scorer(
        set(state["matched"]),
        set(state["partial"]),
        set(state["missing"]),
        state["jd_text"]
    )

    return {
        "score": score
    }