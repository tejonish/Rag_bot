from agents.extractor import run_extractor


def extractor_node(state):

    resume_skills = list(
        run_extractor(state["resume_text"])
    )

    jd_skills = list(
        run_extractor(state["jd_text"])
    )

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills
    }