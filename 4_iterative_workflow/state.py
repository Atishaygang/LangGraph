from typing import TypedDict , Literal

class tweetState(TypedDict):

    # User inputs
    topic: str
    content_type: str
    social_platform: str
    target_audience: str
    tone: str
    language: str
    max_characters: int

    # Workflow outputs
    tweet: str
    evaluation: Literal["approved", "not approved"]
    feedback: str

    # Iterative loop
    iteration: int
    max_iteration: int