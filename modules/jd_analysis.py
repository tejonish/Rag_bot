# modules/jd_analysis.py

from rag_core import get_llm
from sentence_transformers import SentenceTransformer
import numpy as np
import json


# 🧠 LOAD MODEL (once)

model = SentenceTransformer("all-MiniLM-L6-v2")

# 🧠 SKILL EXTRACTION


def extract_skills(text):
    llm = get_llm()

    prompt = f"""
    ```

    Extract ONLY candidate skills from the text.

      STRICT RULES:
      - Only include skills a person can possess or learn
      - Exclude:
        ❌ industries (healthcare, defence, energy)
        ❌ domains (robotics, biotech unless clearly skill-based)
        ❌ project descriptions
        ❌ long phrases (>3 words)
      - Prefer:
        ✔ tools (Python, Git, SQL)
        ✔ techniques (machine learning, deep learning)
        ✔ technologies (LLM, APIs, Docker)

      Return comma-separated list ONLY.

      Text:
      {text}
    """

    res = llm.invoke(prompt).content
    skills = [s.strip().lower() for s in res.split(",") if s.strip()]

    return set(skills)


def clean_skills(skills):
    banned_words = [
        "system",
        "application",
        "platform",
        "technology",
        "industry",
        "domain",
        "environment",
        "solution",
        "security",
        "energy",
        "healthcare",
    ]

    cleaned = set()

    for s in skills:
        if len(s.split()) > 3:
            continue

        if any(b in s for b in banned_words):
            continue

        cleaned.add(s)

    return cleaned


# 🔥 SEMANTIC MATCHING


def semantic_match(
    resume_skills, jd_skills, threshold_match=0.75, threshold_partial=0.55
):

    resume_list = list(resume_skills)
    jd_list = list(jd_skills)

    if not resume_list or not jd_list:
        return set(), set(), set(jd_list)

    resume_emb = model.encode(resume_list, normalize_embeddings=True)
    jd_emb = model.encode(jd_list, normalize_embeddings=True)

    matched = set()
    partial = set()
    missing = set()

    for i, jd_skill in enumerate(jd_list):
        sims = np.dot(resume_emb, jd_emb[i])
        best = float(np.max(sims))

        if best >= threshold_match:
            matched.add(jd_skill)
        elif best >= threshold_partial:
            partial.add(jd_skill)
        else:
            missing.add(jd_skill)

    return matched, partial, missing


# 🧠 JD CLASSIFICATION


def classify_jd_skills(jd_text):
    llm = get_llm()

    prompt = f"""
    

    Extract skills from the job description and classify them.

    Return JSON only:

    {{
    "critical": [...],
    "important": [...],
    "nice": [...]
    }}

    JD:
    {jd_text}
    """

    res = llm.invoke(prompt).content.strip()
    res = res.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(res)
    except:
        return {"critical": set(), "important": set(), "nice": set()}

    return {
        "critical": set(data.get("critical", [])),
        "important": set(data.get("important", [])),
        "nice": set(data.get("nice", [])),
    }


import re


def normalize(skill):
    skill = skill.lower().strip()

    # remove special characters
    skill = re.sub(r"[^a-z0-9\s\+\#\.]", "", skill)

    # collapse spaces
    skill = re.sub(r"\s+", " ", skill)

    return skill


def deduplicate(skills):
    seen = set()
    result = set()

    for s in skills:
        if s not in seen:
            result.add(s)
            seen.add(s)

    return result


# 🚀 MAIN FUNCTION


def analyze_job_fit(resume_text, job_description):

    llm = get_llm()

    # 🔹 Step 1: Extract skills
    resume_skills = clean_skills(extract_skills(resume_text))
    jd_skills = clean_skills(extract_skills(job_description))

    resume_skills = set(normalize(s) for s in resume_skills)
    jd_skills = set(normalize(s) for s in jd_skills)

    # 🔹 Step 2: Semantic matching
    matched, partial, missing = semantic_match(resume_skills, jd_skills)

    # 🔹 Step 3: Dynamic scoring
    jd_categories = classify_jd_skills(job_description)

    critical_missing = missing & jd_categories["critical"]
    important_missing = missing & jd_categories["important"]
    nice_missing = missing & jd_categories["nice"]

    score = 100
    score -= len(critical_missing) * 12
    score -= len(important_missing) * 6
    score -= len(nice_missing) * 2
    score -= len(partial) * 3

    score = max(60, min(score, 85))

    # 🔹 Step 4: Explanation
    prompt = f"""
      

      You are a STRICT AI hiring evaluator.

      DO NOT modify skill lists.

      Matched Skills: {list(matched)}
      Partial Skills: {list(partial)}
      Missing Skills: {list(missing)}

      Score: {score}

      Return:

      🎯 Fit Score: {score}

      ✅ Matching Skills:

      * skill1
      * skill2

      ⚠️ Partially Matching Skills:

      * skill1

      ❌ Missing Skills:

      * skill1

      💡 Hiring Recommendation:

      * 3 concise bullet points
        """

    res = llm.invoke(prompt)

    return res.content
