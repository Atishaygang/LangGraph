from state import tweetState
from llm_model import generation_model , evaluation_model , optimization_model
from prompt import generation_prompt , evaluation_prompt , parser , optimization_prompt



def gen_tweet(state: tweetState):

    prompt = generation_prompt.invoke({
        "topic": state["topic"],
        "content_type": state["content_type"],
        "social_platform": state["social_platform"],
        "target_audience": state["target_audience"],
        "tone": state["tone"],
        "language": state["language"],
        "max_characters": state["max_characters"]
    })

    response = generation_model.invoke(prompt)

    return {
        "tweet": response.content
    }

def evl_tweet(state:tweetState):
    prompt = evaluation_prompt.invoke({
        'tweet': state['tweet']
    })
    response = evaluation_model.invoke(prompt)
    str_res = parser.parse(response.content)
    return {'evaluation': str_res.evaluation,
            'feedback': str_res.feedback
            }

def opt_tweet(state:tweetState):
    prompt = optimization_prompt.invoke({
        "tweet": state['tweet'],
        "evaluation": state['feedback']
    })
    response = optimization_model.invoke(prompt).content
    iteration = state['iteration'] +1

    return { 'tweet': response , 'iteration': iteration}


def route_eval(state:tweetState):
    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    else:
        return 'not approved'
    
