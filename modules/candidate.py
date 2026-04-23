from rag_core import get_llm


def resume_feedback(resume_text):
    llm = get_llm()
    prompt = f"""
Analyze resume:

Give:
- Strengths
- Weaknesses
- Improvements

Resume:
{resume_text}
"""
    return llm.invoke(prompt).content


def generate_questions(resume_text):
    llm = get_llm()
    prompt = f"""
Generate 5 interview questions:
- 2 technical
- 2 project
- 1 HR

Resume:
{resume_text}
"""
    return llm.invoke(prompt).content


def evaluate_answer(question, answer):
    llm = get_llm()
    prompt = f"""
Evaluate answer:

Score (0-10)
Feedback
Better answer

Q: {question}
A: {answer}
"""
    return llm.invoke(prompt).content