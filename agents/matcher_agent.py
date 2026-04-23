# from modules.jd_analysis import semantic_match

# def run_matcher(resume_skills, jd_skills):
#     return semantic_match(resume_skills, jd_skills)

from agents.embedding_model import compute_similarity

def run_matcher(resume_skills, jd_skills):
    matched, partial, missing = compute_similarity(resume_skills, jd_skills)
    return matched, partial, missing