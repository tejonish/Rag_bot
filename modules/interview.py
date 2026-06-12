# modules/interview.py


from rag_core import get_llm

# def generate_question(resume_text, jd_text):
#     llm = get_llm()

#     prompt = f"""
#         You are a technical interviewer.

#         Generate ONE interview question.

#         Priority:
#         1. Missing skills from JD
#         2. Resume projects
#         3. Technical concepts

#         Maximum 15 words.

#         Resume:
#         {resume_text}

#         Job Description:
#         {jd_text}
#         """
#     return llm.invoke(prompt).content.strip()


def generate_questions(resume_text, jd_text):

    llm = get_llm()

    prompt = f"""
            Generate exactly 8 interview questions.

            Rules:
            - 1 Introduction question
            - 4 Technical questions
            - 3 Behavioral questions
            - One question per line
            - No numbering

            Resume:
            {resume_text}

            Job Description:
            {jd_text}
            """

    response = llm.invoke(prompt).content.strip()

    questions = [q.strip() for q in response.split("\n") if q.strip()]

    return questions


def evaluate_answer(question, answer):
    llm = get_llm()

    prompt = f"""
        You are a friendly technical interviewer.

        Evaluate the answer realistically.

        Scoring rules:

        - Do NOT penalize grammar heavily.
        - Focus on technical aspect.
        - Focus on confidence and intent.
        - Spoken interview answers are naturally informal.
        - Reward passion and motivation.
        - Be constructive, not harsh.

        Return:

        Score: x/10

        Good:
        - one strength

        Improve:
        - one improvement

        Question:
        {question}

        Answer:
        {answer}
        """

    return llm.invoke(prompt).content
