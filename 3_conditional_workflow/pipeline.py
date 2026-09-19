from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from state import DSAState

from function import (
    easy_question,
    medium_question,
    tough_question,
    get_user_answer,
    answer_analysis,
    correct_answer,
    wrong_answer,
    final_solution
)


# =========================================================
# ROUTERS
# =========================================================

def difficulty_router(state: DSAState):

    difficulty = state["difficulty"].strip().lower()

    if difficulty == "easy":
        return "easy"

    elif difficulty == "medium":
        return "medium"

    elif difficulty == "tough":
        return "tough"

    else:
        raise ValueError(
            "Difficulty must be easy, medium or tough."
        )


def answer_router(state: DSAState):

    if state["is_correct"]:
        return "correct"

    return "wrong"


def attempt_router(state: DSAState):

    if state["attempts"] >= 3:
        return "final_solution"

    return "retry"


# =========================================================
# GRAPH
# =========================================================

graph = StateGraph(DSAState)


# =========================================================
# NODES
# =========================================================

graph.add_node(
    "easy_question",
    easy_question
)

graph.add_node(
    "medium_question",
    medium_question
)

graph.add_node(
    "tough_question",
    tough_question
)

graph.add_node(
    "get_user_answer",
    get_user_answer
)

graph.add_node(
    "answer_analysis",
    answer_analysis
)

graph.add_node(
    "correct_answer",
    correct_answer
)

graph.add_node(
    "wrong_answer",
    wrong_answer
)

graph.add_node(
    "final_solution",
    final_solution
)


# =========================================================
# DIFFICULTY ROUTING
# =========================================================

graph.add_conditional_edges(
    START,
    difficulty_router,
    {
        "easy": "easy_question",
        "medium": "medium_question",
        "tough": "tough_question"
    }
)


# =========================================================
# QUESTION -> USER ANSWER
# =========================================================

graph.add_edge(
    "easy_question",
    "get_user_answer"
)

graph.add_edge(
    "medium_question",
    "get_user_answer"
)

graph.add_edge(
    "tough_question",
    "get_user_answer"
)


# =========================================================
# USER ANSWER -> ANALYSIS
# =========================================================

graph.add_edge(
    "get_user_answer",
    "answer_analysis"
)


# =========================================================
# CORRECT / WRONG ROUTING
# =========================================================

graph.add_conditional_edges(
    "answer_analysis",
    answer_router,
    {
        "correct": "correct_answer",
        "wrong": "wrong_answer"
    }
)


# =========================================================
# CORRECT -> END
# =========================================================

graph.add_edge(
    "correct_answer",
    END
)


# =========================================================
# WRONG -> RETRY OR FINAL SOLUTION
# =========================================================

graph.add_conditional_edges(
    "wrong_answer",
    attempt_router,
    {
        "retry": "get_user_answer",
        "final_solution": "final_solution"
    }
)


graph.add_edge(
    "final_solution",
    END
)


# =========================================================
# COMPILE
# =========================================================

memory = InMemorySaver()

workflow = graph.compile(
    checkpointer=memory
)