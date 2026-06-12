from langgraph.graph import StateGraph, END

from langgraph_version.graph_state import HiringState

from langgraph_version.nodes.extractor_node import extractor_node
from langgraph_version.nodes.matcher_node import matcher_node
from langgraph_version.nodes.scorer_node import scorer_node
from langgraph_version.nodes.roadmap_node import roadmap_node
from langgraph_version.nodes.formatter_node import formatter_node

from langgraph_version.routers import route_after_scoring


builder = StateGraph(HiringState)

# Nodes
builder.add_node("extractor", extractor_node)
builder.add_node("matcher", matcher_node)
builder.add_node("scorer", scorer_node)
builder.add_node("roadmap", roadmap_node)
builder.add_node("formatter", formatter_node)

# Start
builder.set_entry_point("extractor")

# Normal flow
builder.add_edge("extractor", "matcher")
builder.add_edge("matcher", "scorer")

# Conditional routing
builder.add_conditional_edges(
    "scorer",
    route_after_scoring,
    {
        "roadmap": "roadmap",
        "formatter": "formatter"
    }
)

builder.add_edge("roadmap", "formatter")

builder.add_edge("formatter", END)

graph = builder.compile()