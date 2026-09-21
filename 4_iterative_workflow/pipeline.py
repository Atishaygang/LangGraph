from langgraph.graph import StateGraph , START , END
from state import tweetState
from function import gen_tweet , evl_tweet , opt_tweet , route_eval


# Def graph
graph = StateGraph(tweetState)

# Def Node
graph.add_node('gen_node', gen_tweet)
graph.add_node('evl_node', evl_tweet)
graph.add_node('opt_node', opt_tweet)

# Def edges
graph.add_edge(START, 'gen_node')
graph.add_edge('gen_node' , 'evl_node')
graph.add_conditional_edges('evl_node', route_eval , {'approved' : END , 'not approved': 'opt_node'})
graph.add_edge('opt_node','evl_node')

workflow = graph.compile()

