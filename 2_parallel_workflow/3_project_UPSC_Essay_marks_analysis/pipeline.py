from langgraph.graph import StateGraph , START , END
from typing import TypedDict,Annotated
import operator
from state import UPSC_State
from functions import eval_lang , eval_thg , eval_anl , final_eval
from load_text import essay



#def graph:
graph = StateGraph(UPSC_State)

#def node
graph.add_node('evaluate_language' , eval_lang)
graph.add_node('evaluate_thought' , eval_thg)
graph.add_node('evaluate_analysis' , eval_anl)
graph.add_node('final_evaluation' , final_eval)

# Parallel branches
graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_thought")
graph.add_edge(START, "evaluate_analysis")

# Join all three into final evaluation
graph.add_edge(
    ["evaluate_language", "evaluate_thought", "evaluate_analysis"],
    "final_evaluation"
)

graph.add_edge("final_evaluation", END)

workflow = graph.compile()



result = workflow.invoke({
    "essay": essay
})

final_result = {
    "summary_feedback": result["overall_feedback"],
    "avg_score": result["avg_score"],
    "individual_score": result["individual_score"]
}
print(final_result)
