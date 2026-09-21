from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import Field , BaseModel
from typing import Literal
from state import tweetState

class tweeteval(BaseModel):
    evaluation: Literal["approved", "not approved"] = Field(..., description='evidence')
    feedback: str = Field(..., description= 'feedback of token')

parser = PydanticOutputParser(pydantic_object= tweeteval)


generation_prompt = PromptTemplate(
    template= """You are an expert content writer and social media copywriter.

Create content using the following details:

Topic: {topic}
Content Type: {content_type}
Social Platform: {social_platform}
Target Audience: {target_audience}
Tone: {tone}
Language: {language}
Maximum Characters: {max_characters}

Instructions:

1. Write specifically for the given social platform and follow the writing style that naturally performs well on that platform.

2. Adapt the structure according to the content type.
   For example:
   - Post → concise, engaging, easy to scan
   - Caption → short, catchy, expressive
   - Blog → structured, informative, detailed
   - Article → clear, professional, well organized

3. Write specifically for the target audience. Use vocabulary, depth, examples, and explanation appropriate for them.

4. Maintain the requested tone consistently throughout the content.

5. Start with a strong and relevant opening that immediately attracts attention.

6. Keep the writing natural, human-like, clear, and engaging. Avoid robotic language, unnecessary filler, and repetition.

7. Maintain logical flow between sentences and paragraphs.

8. If Maximum Characters is provided, strictly ensure that the complete output stays within that character limit.
   If no limit is provided, choose an appropriate length based on the content type and platform.

9. Write entirely in the requested language unless commonly used technical terms or names require otherwise.

10. Do not invent facts or statistics. If the topic requires factual claims that are not provided, avoid unsupported specific claims.

11. Do not explain your reasoning or the instructions.

12. Return only the final generated content.

Generate the content now.
""",
    input_variables = [
        "topic",
        "content_type",
        "social_platform",
        "target_audience",
        "tone",
        "language",
        "max_characters"
        ]
)

evaluation_prompt = PromptTemplate(
    template="""
You are an expert social media content evaluator.

Evaluate the following tweet carefully and objectively.

Tweet: {tweet}

Evaluate it based on:

1. Clarity
2. Grammar
3. Readability
4. Engagement
5. Naturalness
6. Strength of the opening
7. Flow
8. Repetition
9. Conciseness
10. Overall effectiveness as a tweet

Also check whether:
- The tweet feels natural and human-written.
- The message is easy to understand.
- There are unnecessary words or sentences.
- The tweet is engaging enough to hold attention.
- The wording can be made sharper or more impactful.
- There are any grammatical or structural problems.

Return your evaluation in exactly this format:

Overall Score: <score out of 10>

Strengths:
- <strength 1>
- <strength 2>

Problems:
- <problem 1>
- <problem 2>

Required Improvements:
- <improvement 1>
- <improvement 2>

Verdict: <GOOD or NEEDS_OPTIMIZATION>

Do not rewrite the tweet.
Only evaluate it.
\n {format_instruction}
""",
    input_variables=["tweet"],
    partial_variables= {
                "format_instruction": parser.get_format_instructions()
            }
)

optimization_prompt = PromptTemplate(
    template="""
You are an expert social media content optimizer.

Your task is to improve the tweet using the evaluation feedback.

Original Tweet:
{tweet}

Evaluation:
{evaluation}

Instructions:

1. Fix the problems identified in the evaluation.

2. Preserve the original meaning and intent of the tweet.

3. Keep the strong parts of the original tweet whenever possible.

4. Improve:
   - Clarity
   - Grammar
   - Readability
   - Engagement
   - Naturalness
   - Flow
   - Conciseness
   - Overall impact

5. Remove unnecessary words, repetition, awkward phrasing, and robotic language.

6. Make the opening stronger if the evaluation suggests it is weak.

7. Keep the tweet natural, human-written, and suitable for social media.

8. Do not add unsupported facts or statistics.

9. Do not mention the evaluation, scores, problems, or optimization process.

10. Return only the optimized tweet.

Optimize the tweet now.
""",
    input_variables=[
        "tweet",
        "evaluation"
    ]
)