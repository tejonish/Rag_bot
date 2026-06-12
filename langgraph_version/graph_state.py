from typing import TypedDict


class HiringState(TypedDict):

    resume_text: str
    jd_text: str

    resume_skills: list
    jd_skills: list

    matched: list
    partial: list
    missing: list

    score: int
    coverage: int

    roadmap: str
    result: str