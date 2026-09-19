from llm_model import llm_model

from Evalutaion_pydatic_schema import parser
from state import UPSC_State
from langchain_core.prompts import PromptTemplate


def eval_lang(state: UPSC_State) -> UPSC_State:

    prompt_template = PromptTemplate(
        template="""
Evaluate the language quality of the following essay:

{essay}

Provide feedback and assign a score out of 10.

{format_instruction}
""",
        input_variables=["essay"],
        partial_variables={
            "format_instruction": parser.get_format_instructions()
        }
    )

    prompt = prompt_template.invoke({
        "essay": state["essay"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    return {
        "lang_feedback": parsed_output.feedback,
        "individual_score": [parsed_output.score]
    }


def eval_thg(state: UPSC_State) -> UPSC_State:

    prompt_template = PromptTemplate(
        template="""
Evaluate the thought quality and clarity of the following essay:

{essay}

Provide feedback and assign a score out of 10.

{format_instruction}
""",
        input_variables=["essay"],
        partial_variables={
            "format_instruction": parser.get_format_instructions()
        }
    )

    prompt = prompt_template.invoke({
        "essay": state["essay"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    return {
        "clarity_feedback": parsed_output.feedback,
        "individual_score": [parsed_output.score]
    }


def eval_anl(state: UPSC_State) -> UPSC_State:

    prompt_template = PromptTemplate(
        template="""
Evaluate the depth of analysis of the following essay:

{essay}

Provide feedback and assign a score out of 10.

{format_instruction}
""",
        input_variables=["essay"],
        partial_variables={
            "format_instruction": parser.get_format_instructions()
        }
    )

    prompt = prompt_template.invoke({
        "essay": state["essay"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    return {
        "analysis_feedback": parsed_output.feedback,
        "individual_score": [parsed_output.score]
    }


def final_eval(state: UPSC_State) -> UPSC_State:

    prompt_template = PromptTemplate(
        template="""
Based on the following feedbacks, create a summarized final feedback.

Analysis feedback:
{analysis_feedback}

Language feedback:
{lang_feedback}

Clarity feedback:
{clarity_feedback}

{format_instruction}
""",
        input_variables=[
            "analysis_feedback",
            "lang_feedback",
            "clarity_feedback"
        ],
        partial_variables={
            "format_instruction": parser.get_format_instructions()
        }
    )

    prompt = prompt_template.invoke({
        "analysis_feedback": state["analysis_feedback"],
        "lang_feedback": state["lang_feedback"],
        "clarity_feedback": state["clarity_feedback"]
    })

    output = llm_model.invoke(prompt)

    parsed_output = parser.parse(output.content)

    avg_score = sum(state["individual_score"]) / len(state["individual_score"])

    return {
    "overall_feedback": parsed_output.feedback,
    "avg_score": avg_score
    }

