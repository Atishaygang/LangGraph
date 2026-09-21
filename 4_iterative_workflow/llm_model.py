from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

g_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-8B",
    
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )
)

e_llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )
)

o_llm = HuggingFaceEndpoint(
    repo_id="google/gemma-3-12b-it",
    
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )
)
generation_model = ChatHuggingFace(llm=g_llm)
evaluation_model = ChatHuggingFace(llm=e_llm)
optimization_model = ChatHuggingFace(llm=o_llm)