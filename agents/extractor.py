from modules.jd_analysis import extract_skills, clean_skills, normalize

def run_extractor(text):
    skills = clean_skills(extract_skills(text))
    skills = set(normalize(s) for s in skills)
    return skills