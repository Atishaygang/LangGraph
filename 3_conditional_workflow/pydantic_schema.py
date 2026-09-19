from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class QuestionSchema(BaseModel):

    question: str = Field(
        description="Complete DSA question including title, problem statement, constraints and examples"
    )


parser = PydanticOutputParser(
    pydantic_object=QuestionSchema
)


class AnswerAnalysis(BaseModel):

    is_correct: bool = Field(
        description="True if the user's solution is correct, otherwise False"
    )

    feedback: str = Field(
        description="Explanation of why the answer is correct or where it went wrong"
    )

    hint: str = Field(
        description="A hint for the next attempt if wrong, otherwise empty string"
    )


answer_parser = PydanticOutputParser(
    pydantic_object=AnswerAnalysis
)