# modules/ats.py

from rag_core import get_llm

def ats_score(resume_text, jd):
    llm = get_llm()

    prompt = f"""
You are an ATS system.

Return STRICT FORMAT (no paragraphs):

ATS Score: <number>/100
Keyword Match: <number>%
Missing: <max 5 comma-separated keywords>
Suggestions: <max 3 short bullet points>

Rules:
- Keep output under 5 lines
- No explanations
- No paragraphs

Resume:
{resume_text}

JD:
{jd}
"""

    return llm.invoke(prompt).content.strip()