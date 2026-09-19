from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    provider="cerebras",
    task="text-generation",
    max_new_tokens=1000,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_ACCESS_TOKEN"
    )
)

llm_model = ChatHuggingFace(llm=llm)