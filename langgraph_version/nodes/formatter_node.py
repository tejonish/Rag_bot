from agents.formatter_agent import format_output


def formatter_node(state):

    result = format_output(
        state["matched"],
        state["partial"],
        state["missing"],
        state["score"],
        state["coverage"]
    )

    # roadmap may or may not exist
    if state.get("roadmap"):
        result += (
            "\n\n📚 Learning Roadmap:\n"
            + state["roadmap"]
        )

    return {
        "result": result
    }