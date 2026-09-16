from langgraph.graph import StateGraph , START , END
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
    max_new_tokens=2000,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )
)

llm_model = ChatHuggingFace(llm=llm)

# defining State
class StateBlog(TypedDict):
    topic: str
    outline: str
    blog: str

#def function
def crt_out(state:StateBlog) -> StateBlog:
    topic = state['topic']
    prompt = f'Create a outline on the {topic}'
    outline = llm_model.invoke(
        prompt
    ).content
    state['outline'] = outline
    return {"outline": outline}

def crt_blog(state:StateBlog) -> StateBlog:
    outline = state['outline']
    prompt = f'Create a research on the {outline}'
    blog = llm_model.invoke(
        prompt
    ).content
    state['blog'] = blog
    return {"blog": blog}




# Def Graph
graph = StateGraph(StateBlog)

#Def node
graph.add_node('Create_outline' , crt_out)
graph.add_node('create_blog',crt_blog)

#def edge
graph.add_edge(START, 'Create_outline')
graph.add_edge('Create_outline','create_blog')
graph.add_edge('create_blog' , END)

#Compile
workflow = graph.compile()

result = workflow.invoke({
    "topic" : 'AI and India'
})

print(result)