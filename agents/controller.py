# from agents.extractor import run_extractor
# from agents.matcher_agent import run_matcher
# from agents.scorer_agent import run_scorer
# from agents.formatter_agent import format_output
# from agents.roadmap_agent import generate_roadmap

# def run_pipeline(resume_text, jd_text):

#     resume_skills = run_extractor(resume_text)
#     jd_skills = run_extractor(jd_text)

#     matched, partial, missing = run_matcher(resume_skills, jd_skills)

#     coverage = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

#     score = run_scorer(matched, partial, missing, jd_text)

#     result = format_output(matched, partial, missing, score, coverage)

#     roadmap = generate_roadmap(missing)

#     result += "\n\n📚 Learning Roadmap:\n"
#     result += roadmap

#     return result

from rag_core import get_llm
from agents.extractor import run_extractor
from agents.matcher_agent import run_matcher
from agents.scorer_agent import run_scorer
from agents.formatter_agent import format_output
from agents.roadmap_agent import generate_roadmap


def run_pipeline(resume_text, jd_text):

    llm = get_llm()

    # =========================
    # LLM CONTROLLER
    # =========================

    decision_prompt = """
    You are an AI controller.

    Always return steps in this exact format:
    extract, match, score, roadmap

    Rules:
    - Only use these words
    - Must be comma-separated
    - No explanations

    If unsure, return:
    extract, match, score, roadmap
    """

    decision = ""

    try:
        response = llm.invoke(decision_prompt)
        decision = getattr(response, "content", "").lower()
    except:
        decision = ""

    allowed = {"extract", "match", "score", "roadmap"}

    steps = [s.strip() for s in decision.split(",") if s.strip() in allowed]

    # fallback safety
    if not steps:
        steps = ["extract", "match", "score", "roadmap"]

    # =========================
    # EXECUTION PIPELINE
    # =========================

    resume_skills = None
    jd_skills = None

    matched = set()
    partial = set()
    missing = set()

    score = 0
    coverage = 0

    # 🔹 Extract
    if "extract" in steps:
        resume_skills = run_extractor(resume_text)
        jd_skills = run_extractor(jd_text)

    # 🔹 Match
    if "match" in steps and resume_skills and jd_skills:
        matched, partial, missing = run_matcher(resume_skills, jd_skills)

        if jd_skills:
            coverage = int((len(matched) / len(jd_skills)) * 100)

    # 🔹 Score
    if "score" in steps:
        score = run_scorer(matched, partial, missing, jd_text)

    # 🔹 Format Output
    result = format_output(matched, partial, missing, score, coverage)

    # 🔹 Roadmap
    if "roadmap" in steps:
        top_missing = list(missing)[:4]

        roadmap = generate_roadmap(
            missing_skills=top_missing, known_skills=matched, partial_skills=partial
        )
        result += "\n\n📚 Learning Roadmap:\n" + roadmap

    return result, steps
