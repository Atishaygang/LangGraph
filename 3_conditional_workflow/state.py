from typing import TypedDict

class DSAState(TypedDict):
    topic: str
    difficulty: str
    question: str
    user_answer: str
    is_correct: bool
    attempts: int
    hint: str
    feedback: str
    score: int
    total_correct: int
    total_questions: int
    
    response: str