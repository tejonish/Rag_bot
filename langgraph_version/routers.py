def route_after_scoring(state):

    if state["score"] >= 80:
        return "formatter"

    return "roadmap"