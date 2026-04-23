# modules/resume.py

from rag_core import build_rag_chain, summarize_resume, extract_full_text, get_llm
import re


def resume_qa_tool(pdf_path, question):
    """
    Wrapper for RAG Q&A
    """
    rag_chain = build_rag_chain(pdf_path)
    result = rag_chain.invoke({"input": question})
    return result


def resume_summary_tool(pdf_path):
    """
    Wrapper for full resume summary
    """
    return summarize_resume(pdf_path)


# 🔥 NEW FUNCTION (IMPORTANT)
def resume_feedback_tool(pdf_path):
    """
    Generate structured resume feedback (NOT summary)
    """
    text = extract_full_text(pdf_path)
    llm = get_llm()

    prompt = f"""
You are a senior AI recruiter.

Analyze the resume and return STRICT FORMAT:

Strengths:
- (max 4)

Weaknesses:
- (max 4)

Missing Skills:
- (max 5)

Improvements:
- (max 4 actionable points)

Rules:
- Be strict
- No paragraphs
- Bullet points only

Resume:
{text}
"""

    return llm.invoke(prompt).content.strip()


def extract_github_from_resume(pdf_path):
    """
    Extract GitHub username from resume text (robust + safe)
    """
    text = extract_full_text(pdf_path)

    # normalize
    text = text.lower().replace("https://", "").replace("http://", "")

    patterns = [
        r"github\.com/([a-z0-9_-]+)",
        r"github\.com/([a-z0-9_-]+)/",
        r"github[:\s]+([a-z0-9_-]+)",
        r"github username[:\s]+([a-z0-9_-]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None