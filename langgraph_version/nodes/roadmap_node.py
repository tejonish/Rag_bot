# nodes/roadmap_node.py

from agents.roadmap_agent import generate_roadmap


def roadmap_node(state):

    roadmap = generate_roadmap(
        missing_skills=set(state["missing"]),
        known_skills=set(state["matched"]),
        partial_skills=set(state["partial"])
    )

    return {
        "roadmap": roadmap
    }