from modules.intents import detect_intent
from rag_core import get_llm


def candidate_assistant(
    query,
    resume_text,
    fit_report,
    chat_history=None
):

    intent = detect_intent(query)

    if intent == "FIT_SCORE":

        llm = get_llm()

        prompt = f"""
Explain the fit score briefly.

Fit Report:
{fit_report}

Question:
{query}

Rules:
- Max 5 lines
- Mention strengths
- Mention missing skills
- Do not print full report
"""

        return intent, llm.invoke(prompt).content

    elif intent == "MISSING_SKILLS":

        llm = get_llm()

        prompt = f"""
Extract only missing skills.

Fit Report:
{fit_report}
"""

        return intent, llm.invoke(prompt).content

    elif intent == "ROADMAP":

        llm = get_llm()

        prompt = f"""
Give top 3 skills to learn first.

Fit Report:
{fit_report}

Keep concise.
"""

        return intent, llm.invoke(prompt).content

    else:

        llm = get_llm()

        return intent, llm.invoke(
            f"""
        Resume:
        {resume_text}

        Fit Report:
        {fit_report}

        Conversation History:
        {chat_history}

        Question:
        {query}

        Answer briefly.
        """
        ).content