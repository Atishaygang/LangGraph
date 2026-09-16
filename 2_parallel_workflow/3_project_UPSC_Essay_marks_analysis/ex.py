from llm_model import llm_model

response = llm_model.invoke("Say hello in one sentence.")
print(response.content)