# LangGraph Workflows — Sequential & Parallel

This repository documents two hands-on LangGraph workflow patterns:

1. **Sequential Workflow** — Blog generation pipeline
2. **Parallel Workflow** — UPSC essay evaluation pipeline

The goal is to understand how **state moves through nodes**, how nodes execute one after another, and how multiple branches can run in parallel before joining into a final node.

---

## 1. Sequential Workflow

### Use Case

Generate a blog in two stages:

1. Create an outline from a topic.
2. Generate the final blog using that outline.

### Workflow

```text
START
  ↓
Create Outline
  ↓
Create Blog
  ↓
END
```

### State

```python
from typing import TypedDict

class BlogState(TypedDict):
    topic: str
    outline: str
    blog: str
```

### Node 1 — Create Outline

```python
def create_outline(state: BlogState):
    topic = state["topic"]

    prompt = f"Create an outline for a blog on: {topic}"
    outline = llm_model.invoke(prompt).content

    return {"outline": outline}
```

### Node 2 — Create Blog

```python
def create_blog(state: BlogState):
    outline = state["outline"]

    prompt = f"Write a detailed blog based on this outline:\n\n{outline}"
    blog = llm_model.invoke(prompt).content

    return {"blog": blog}
```

### Graph Construction

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(BlogState)

graph.add_node("create_outline", create_outline)
graph.add_node("create_blog", create_blog)

graph.add_edge(START, "create_outline")
graph.add_edge("create_outline", "create_blog")
graph.add_edge("create_blog", END)

workflow = graph.compile()
```

### Execute

```python
result = workflow.invoke({
    "topic": "AI and India"
})

print(result)
```

### What This Taught Me

- Defining shared state using `TypedDict`
- Creating nodes as Python functions
- Reading values from state
- Returning state updates from nodes
- Connecting nodes with edges
- Compiling and invoking a LangGraph workflow
- Passing one node's output into the next node

---

## 2. Parallel Workflow

### Use Case

Evaluate a UPSC essay from three independent perspectives:

- Language quality
- Thought / clarity quality
- Depth of analysis

Each evaluator returns written feedback and a score out of 10. After all three branches finish, a final node summarizes the feedback and Python calculates the average score.

### Workflow

```text
                       ┌── Evaluate Language ──┐
                       │                       │
START ─────────────────┼── Evaluate Thought ───┼──→ Final Evaluation ──→ END
                       │                       │
                       └── Evaluate Analysis ──┘
```

### State

```python
from typing import TypedDict, Annotated
import operator

class UPSC_State(TypedDict):
    essay: str
    lang_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_score: Annotated[list[int], operator.add]
    avg_score: float
```

### Why `Annotated + operator.add`?

All three parallel branches write to the same `individual_score` key.

```python
individual_score: Annotated[list[int], operator.add]
```

This lets LangGraph merge values like:

```python
[8] + [7] + [9]
```

into:

```python
[8, 7, 9]
```

instead of creating a conflicting parallel update.

---

## Structured Output

A Pydantic schema is used so each evaluator returns a predictable structure.

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class EvaluationSchema(BaseModel):
    feedback: str = Field(description="Written feedback for the essay")
    score: int = Field(description="Score for the essay", ge=0, le=10)

parser = PydanticOutputParser(pydantic_object=EvaluationSchema)
```

The model returns an `AIMessage`, so its text must be parsed before accessing structured fields:

```python
output = llm_model.invoke(prompt)
parsed_output = parser.parse(output.content)
```

---

## Parallel Evaluator Pattern

Example language evaluator:

```python
def eval_lang(state: UPSC_State):
    prompt_template = PromptTemplate(
        template="""
Evaluate the language quality of the following essay:

{essay}

Provide feedback and assign a score out of 10.

{format_instruction}
""",
        input_variables=["essay"],
        partial_variables={
            "format_instruction": parser.get_format_instructions()
        }
    )

    prompt = prompt_template.invoke({
        "essay": state["essay"]
    })

    output = llm_model.invoke(prompt)
    parsed_output = parser.parse(output.content)

    return {
        "lang_feedback": parsed_output.feedback,
        "individual_score": [parsed_output.score]
    }
```

The thought and analysis evaluators follow the same pattern and write to their own feedback keys.

---

## Final Evaluation

```python
def final_eval(state: UPSC_State):
    prompt_template = PromptTemplate(
        template="""
Based on the following feedbacks, create a summarized final feedback.

Analysis feedback:
{analysis_feedback}

Language feedback:
{lang_feedback}

Clarity feedback:
{clarity_feedback}

{format_instruction}
""",
        input_variables=[
            "analysis_feedback",
            "lang_feedback",
            "clarity_feedback"
        ],
        partial_variables={
            "format_instruction": parser.get_format_instructions()
        }
    )

    prompt = prompt_template.invoke({
        "analysis_feedback": state["analysis_feedback"],
        "lang_feedback": state["lang_feedback"],
        "clarity_feedback": state["clarity_feedback"]
    })

    output = llm_model.invoke(prompt)
    parsed_output = parser.parse(output.content)

    avg_score = sum(state["individual_score"]) / len(state["individual_score"])

    return {
        "overall_feedback": parsed_output.feedback,
        "avg_score": avg_score
    }
```

### Why Calculate the Average in Python?

The LLM should handle qualitative feedback, while Python should handle deterministic arithmetic.

```python
avg_score = sum(state["individual_score"]) / len(state["individual_score"])
```

---

## Parallel Graph Construction

```python
graph = StateGraph(UPSC_State)

graph.add_node("evaluate_language", eval_lang)
graph.add_node("evaluate_thought", eval_thg)
graph.add_node("evaluate_analysis", eval_anl)
graph.add_node("final_evaluation", final_eval)

graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_thought")
graph.add_edge(START, "evaluate_analysis")

graph.add_edge(
    [
        "evaluate_language",
        "evaluate_thought",
        "evaluate_analysis"
    ],
    "final_evaluation"
)

graph.add_edge("final_evaluation", END)

workflow = graph.compile()
```

### Execute

```python
result = workflow.invoke({
    "essay": essay
})
```

### Extract Only the Final Results

```python
final_result = {
    "summary_feedback": result["overall_feedback"],
    "avg_score": result["avg_score"],
    "individual_score": result["individual_score"]
}

print(final_result)
```

Example structure:

```python
{
    "summary_feedback": "...",
    "avg_score": 7.67,
    "individual_score": [8, 7, 8]
}
```

---

## Sequential vs Parallel

| Concept | Sequential Workflow | Parallel Workflow |
|---|---|---|
| Execution | One node after another | Multiple nodes run independently |
| State flow | Output feeds the next node | Branches read common state and write outputs |
| Example | Outline → Blog | Language / Thought / Analysis |
| Join required | No | Yes |
| Reducer required | Usually no | Needed when branches update the same key |
| Best for | Dependent steps | Independent tasks that can run together |

---

## Key Learnings

- `StateGraph` represents the workflow.
- Nodes are Python functions that read state and return updates.
- Edges define execution order.
- Sequential workflows are useful when one step depends on another.
- Parallel workflows are useful when tasks can run independently.
- Parallel writes to the same key need a reducer.
- `PydanticOutputParser` gives predictable LLM output.
- `AIMessage.content` must be parsed before using structured fields.
- LLMs should handle qualitative reasoning; Python should handle exact calculations.
- A final join node can combine outputs from multiple branches.

---

## Learning Progress

```text
LangChain + RAG          ✅
FastAPI + Docker         ✅
LangGraph Theory         ✅
Sequential Workflow      ✅
Parallel Workflow        ✅
Conditional Workflows    ⏳
Tool Calling Graphs      ⏳
Memory / Checkpointing   ⏳
Human-in-the-Loop        ⏳
PolicyIQ Agentic V6      ⏳
```

---

## Author

**Atishay Jain**  
B.Sc. (Hons.) Computer Science & Data Analytics  
IIT Patna

Built while learning LangGraph and Agentic AI through hands-on implementation.
