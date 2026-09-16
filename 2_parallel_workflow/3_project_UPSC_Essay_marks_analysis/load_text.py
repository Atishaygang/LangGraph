from langchain_community.document_loaders import TextLoader

loader = TextLoader(r'D:\GenAI\LangGraph\3_project_UPSC_Essay_marks_analysis\essay.txt')

documents = loader.load()

essay = documents[0].page_content

print(type(essay))