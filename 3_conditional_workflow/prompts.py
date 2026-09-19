from langchain_core.prompts import PromptTemplate
from pydantic_schema import parser, answer_parser

# ---------------- EASY ----------------

easy_prompt = PromptTemplate(
    template="""
You are a DSA instructor.

Generate ONE EASY-level DSA coding question based on the topic:

Topic: {topic}

Requirements:
- The question should test basic understanding of the topic.
- It should be suitable for a beginner.
- Avoid tricky edge cases.
- The expected solution should require simple logic.
- Do NOT provide the solution.
- Do NOT provide hints.
- Clearly mention input, output, and constraints.
- Provide 2 example test cases.

Return only the question in a clean format.
\n {format_instruction}
""",
    input_variables=["topic"],
    partial_variables= {
        "format_instruction": parser.get_format_instructions()
    }
)


# ---------------- MEDIUM ----------------

medium_prompt = PromptTemplate(
    template="""
You are an experienced DSA interviewer.

Generate ONE MEDIUM-level DSA coding question based on the topic:

Topic: {topic}

Requirements:
- The problem should require good understanding of the topic.
- It should require more than a straightforward brute-force approach.
- Include meaningful edge cases.
- The candidate should need to think about time and space complexity.
- Do NOT provide the solution.
- Do NOT provide hints.
- Clearly mention input, output, and constraints.
- Provide 2-3 example test cases.

Return only the question in a clean interview-style format.
\n {format_instruction}
""",
    input_variables=["topic"],
    partial_variables= {
            "format_instruction": parser.get_format_instructions()
        }
)


# ---------------- TOUGH ----------------

tough_prompt = PromptTemplate(
    template="""
You are a senior software engineer conducting a challenging DSA interview.

Generate ONE TOUGH-level DSA coding question based on the topic:

Topic: {topic}

Requirements:
- The problem should require strong problem-solving ability.
- It should involve non-trivial logic or optimization.
- Include tricky edge cases.
- A naive solution should be inefficient.
- The candidate should need to think carefully about optimal
  time and space complexity.
- Do NOT provide the solution.
- Do NOT provide hints.
- Clearly mention input, output, and constraints.
- Provide 2-3 example test cases.
- The problem should be challenging but solvable using the given topic.

Return only the question in a clean interview-style format.
\n {format_instruction}
""",
    input_variables=["topic"],
    partial_variables= {
            "format_instruction": parser.get_format_instructions()
        }
)

answer_analysis_prompt = PromptTemplate(
    template="""
You are an expert DSA interviewer and coding evaluator.

Evaluate the user's submitted solution for the given DSA problem.

Question:
{question}

User Answer:
{user_answer}

Your task:
- Decide whether the answer is correct or wrong.
- Check whether the logic actually solves the problem.
- Consider important edge cases.
- Check whether the approach satisfies the problem requirements.
- Do not mark an answer correct just because the idea sounds reasonable.

If the answer is correct:
- Set is_correct to true.
- Briefly explain why it works.
- Give positive feedback.
- Keep hint empty.

If the answer is wrong:
- Set is_correct to false.
- Explain the main mistake.
- Mention the logical issue or missed edge case.
- Give one useful hint.
- Do NOT reveal the complete solution.

Keep the feedback concise and educational.

{format_instruction}
""",

    input_variables=[
        "question",
        "user_answer"
    ],

    partial_variables={
        "format_instruction": answer_parser.get_format_instructions()
    }
)


correct_answer_prompt = PromptTemplate(
    template="""
You are a supportive DSA mentor.

The user has submitted a CORRECT solution to the following problem.

Question:
{question}

User Answer:
{user_answer}

Analysis Feedback:
{feedback}

Your task:
- Appreciate the user for solving the problem correctly.
- Briefly mention what they did well.
- Keep the response motivating but not overly dramatic.
- Mention one strength of their approach, such as logic, correctness, clarity, or efficiency.
- Do NOT repeat the full solution.
- Keep the response concise.

Return only the final appreciation message.
""",
    input_variables=[
        "question",
        "user_answer",
        "feedback"
    ]
)



wrong_answer_prompt = PromptTemplate(
    template="""
You are a patient DSA mentor.

The user's submitted solution is WRONG for the following problem.

Question:
{question}

User Answer:
{user_answer}

Analysis Feedback:
{feedback}

Hint:
{hint}

Attempt Number:
{attempt}

Your task:
- Explain clearly where the user is going wrong.
- Focus on the main logical mistake.
- Use the provided feedback and hint.
- Do NOT reveal the complete solution.
- Guide the user toward discovering the correction themselves.
- If relevant, mention the kind of edge case or condition they are missing.
- Keep the response concise and educational.
- Encourage another attempt.

Return only the mentor's feedback message.
""",
    input_variables=[
        "question",
        "user_answer",
        "feedback",
        "hint",
        "attempt"
    ]
)

final_solution_prompt = PromptTemplate(
    template="""
You are an expert DSA mentor.

The user has attempted the following problem multiple times but has not reached
the correct solution.

Question:
{question}

User's Latest Answer:
{user_answer}

Previous Feedback:
{feedback}

Your task:
- Explain the correct approach clearly and step by step.
- Explain what concept the user was missing.
- Show why their previous approach failed.
- Provide the optimal reasoning.
- Provide the final correct code solution.
- Explain the time complexity.
- Explain the space complexity.
- Keep the explanation beginner-friendly and structured.

Return the complete learning-oriented solution.
""",
    input_variables=[
        "question",
        "user_answer",
        "feedback"
    ]
)