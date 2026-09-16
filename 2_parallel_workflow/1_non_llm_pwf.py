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
