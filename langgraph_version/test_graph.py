from langgraph_version.hiring_graph import graph

result = graph.invoke(
    {
        "resume_text": """
            Python
            """,
        "jd_text": """
        Python
        LangGraph
        AWS
        Docker
        RAG
        """,
    }
)

print(result)
