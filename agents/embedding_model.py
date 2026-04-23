from sentence_transformers import SentenceTransformer, util

# load once (fast after first run)

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text_list):
    return model.encode(text_list, convert_to_tensor=True)

def compute_similarity(resume_skills, jd_skills, threshold=0.6):
    if not resume_skills or not jd_skills:
        return set(), set(), set(jd_skills)

    res_emb = get_embedding(list(resume_skills))
    jd_emb = get_embedding(list(jd_skills))

    matched = set()
    partial = set()
    missing = set()

    for i, jd_skill in enumerate(jd_skills):
        sims = util.cos_sim(jd_emb[i], res_emb)[0]
        max_sim = float(sims.max())

        if max_sim > 0.75:
            matched.add(jd_skill)
        elif max_sim > threshold:
            partial.add(jd_skill)
        else:
            missing.add(jd_skill)

    return matched, partial, missing

