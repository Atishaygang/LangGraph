from typing import TypedDict, Annotated
import operator


class UPSC_State(TypedDict):
    essay: str

    lang_feedback: str
    analysis_feedback: str
    clarity_feedback: str

    overall_feedback: str

    individual_score: Annotated[list[int], operator.add]

    avg_score: float