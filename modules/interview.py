# modules/interview.py


from rag_core import get_llm


def generate_question(resume_text):
    llm = get_llm()

    prompt = f"""
Generate ONE interview question (max 10 words).

Resume:
{resume_text}
"""
    return llm.invoke(prompt).content.strip()


def evaluate_answer(question, answer):
    llm = get_llm()

    prompt = f"""
Return SHORT:

Score: x/10
Feedback: one line

Q: {question}
A: {answer}
"""
    return llm.invoke(prompt).content
