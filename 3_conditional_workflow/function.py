from llm_model import llm_model

from prompts import (
    easy_prompt,
    medium_prompt,
    tough_prompt,
    answer_analysis_prompt,
    correct_answer_prompt,
    wrong_answer_prompt,
    final_solution_prompt
)

from pydantic_schema import parser
from pydantic_schema import answer_parser
from langgraph.types import interrupt
from state import DSAState


# =========================================================
# EASY QUESTION NODE
# =========================================================




def get_user_answer(state: DSAState):

    user_answer = interrupt({
        "question": state["question"],
        "attempt": state.get("attempts", 0) + 1,
        "message": "Submit your solution"
    })

    return {
        "user_answer": user_answer
    }



def easy_question(state: DSAState):

    prompt = easy_prompt.invoke({
        "topic": state["topic"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    return {
        "question": parsed_output.question
    }


# =========================================================
# MEDIUM QUESTION NODE
# =========================================================

def medium_question(state: DSAState):

    prompt = medium_prompt.invoke({
        "topic": state["topic"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    return {
        "question": parsed_output.question
    }


# =========================================================
# TOUGH QUESTION NODE
# =========================================================

def tough_question(state: DSAState):

    prompt = tough_prompt.invoke({
        "topic": state["topic"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    return {
        "question": parsed_output.question
    }


# =========================================================
# ANSWER ANALYSIS NODE
# =========================================================

def answer_analysis(state: DSAState):

    prompt = answer_analysis_prompt.invoke({
        "question": state["question"],
        "user_answer": state["user_answer"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = answer_parser.parse(output.content)

    return {
        "is_correct": parsed_output.is_correct,
        "feedback": parsed_output.feedback,
        "hint": parsed_output.hint
    }


# =========================================================
# CORRECT ANSWER NODE
# =========================================================

def correct_answer(state: DSAState):

    prompt = correct_answer_prompt.invoke({
        "question": state["question"],
        "user_answer": state["user_answer"],
        "feedback": state["feedback"]
    })

    output = llm_model.invoke(prompt)

    return {
        "response": output.content
    }


# =========================================================
# WRONG ANSWER NODE
# =========================================================

def wrong_answer(state: DSAState):

    prompt = wrong_answer_prompt.invoke({
        "question": state["question"],
        "user_answer": state["user_answer"],
        "feedback": state["feedback"],
        "hint": state["hint"],
        "attempt": state["attempts"]
    })

    output = llm_model.invoke(prompt)

    return {
        "response": output.content,
        "attempts": state["attempts"] + 1
    }


# =========================================================
# FINAL SOLUTION NODE
# =========================================================

def final_solution(state: DSAState):

    prompt = final_solution_prompt.invoke({
        "question": state["question"],
        "user_answer": state["user_answer"],
        "feedback": state["feedback"]
    })

    output = llm_model.invoke(prompt)

    return {
        "response": output.content
    }