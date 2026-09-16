from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class evaluation_schema(BaseModel):
    feedback: str = Field(description= 'written feedback for your essay writing')
    score: int = Field(description='Score for your essay' , ge=0 , le=10)

parser = PydanticOutputParser(pydantic_object=evaluation_schema)