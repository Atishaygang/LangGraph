from langchain_huggingface import HuggingFaceEndpoint , ChatHuggingFace
from langgraph.graph import StateGraph , START , END
from dotenv import load_dotenv
from typing import TypedDict
load_dotenv()
import os

# LLM
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-8B",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )
)

llm_model = ChatHuggingFace(llm=llm)

# Define state
class query_state(TypedDict):
    question: str
    Answer: str

# def func
def llm_qa(state:query_state) -> query_state:
    question = state["question"]

    prompt = f'Answer the following {question}'

    answer = llm_model.invoke(prompt).content

    state["Answer"] = answer

    return state


#def graph
graph = StateGraph(query_state)

# def node
graph.add_node('LLM_bot' , llm_qa)

#def edge
graph.add_edge(START,"LLM_bot")
graph.add_edge("LLM_bot",END)

# compile graph
workflow = graph.compile()

result = workflow.invoke({
    'question': 'How is India as a country'
})

print(result)

