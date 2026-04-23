from modules.jd_analysis import classify_jd_skills

def run_scorer(matched, partial, missing, jd_text):
    jd_categories = classify_jd_skills(jd_text)

    critical_missing = missing & jd_categories["critical"]
    important_missing = missing & jd_categories["important"]
    nice_missing = missing & jd_categories["nice"]

    score = 100
    score -= len(critical_missing) * 12
    score -= len(important_missing) * 6
    score -= len(nice_missing) * 2
    score -= len(partial) * 3

    return max(60, min(score, 85))