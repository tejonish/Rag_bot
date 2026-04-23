from rag_core import get_llm


def generate_roadmap(missing_skills, known_skills,partial_skills):
    if not missing_skills:
        return "No major skill gaps identified."

    # convert set/list → clean string
    missing_skills = ", ".join(sorted(missing_skills))
    known_skills = ", ".join(sorted(known_skills))
    partial_skills=",".join(sorted(partial_skills))

    llm = get_llm()

    prompt = f"""
        You are an expert AI mentor.

        The candidate already has skills in:
        The candidate already has strong skills in: 
        {known_skills}

        Generate a PERSONALIZED learning roadmap.

        For each missing skill:

        * Connect it with what the candidate already knows
        * Make learning path realistic
        * Suggest practical steps

        Format:

        skill →

        * Learn: (1 short line)
        * Project: (1 short line)

        Skills:
        {missing_skills}

        Rules:
        

        * Avoid generic advice
        * Relate to existing skills
        * Focus on real-world applications
        * Max 2 lines per skill
        * Only top important skills
        * No explanations
        * Be concise  
        """

    try:
        res = llm.invoke(prompt)
        output = getattr(res, "content", "").strip()
    except:
        output = ""

    # fallback (important)
    if not output:
        return "Unable to generate roadmap right now. Please try again."

    return output
