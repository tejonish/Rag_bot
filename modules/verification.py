# modules/verification.py

from modules.github import github_tool
from rag_core import get_llm


def verify_resume_with_github(resume_text, github_username):
    """
    Compare resume content with GitHub repos
    """

    # 🔹 Fetch GitHub data
    github_data = github_tool(github_username)

    llm = get_llm()

    # 🔥 IMPROVED PROMPT
    prompt = f"""
You are an expert AI recruiter.

Compare the candidate's resume with their GitHub profile.

IMPORTANT RULES:
- Consider semantic similarity (not exact keyword match)
- If a project indirectly shows a skill, count it as PARTIAL
- Do NOT falsely mark skills as missing
- Be fair, realistic, and practical (like a real recruiter)

Return STRICTLY in this format:

🔍 Verification Report

✅ Verified Skills:
- skill 1
- skill 2

⚠️ Partially Verified Skills:
- skill 1
- skill 2

❌ Missing Skills:
- skill 1
- skill 2

⚠️ Weak Areas:
- point 1
- point 2

📊 Trust Score:
<number between 0-100>

🚀 Suggestions:
- suggestion 1
- suggestion 2


Resume:
{resume_text}

GitHub:
{github_data}
"""

    response = llm.invoke(prompt)

    return response.content