import streamlit as st

from pipeline import workflow


st.set_page_config(
    page_title="Iterative Content Optimizer",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ Iterative Content Optimizer")
st.caption(
    "Generate → Evaluate → Optimize → Re-evaluate using an iterative LangGraph workflow."
)

with st.form("content_form"):
    topic = st.text_area(
        "Topic",
        placeholder="Example: Why learning DSA alongside GenAI is useful",
        height=120,
    )

    col1, col2 = st.columns(2)

    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Post", "Caption", "Tweet", "Article", "Blog"],
        )

        social_platform = st.selectbox(
            "Social Platform",
            ["LinkedIn", "X / Twitter", "Instagram", "General"],
        )

        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Conversational",
                "Educational",
                "Motivational",
                "Technical",
                "Casual",
            ],
        )

    with col2:
        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: AI/ML students and developers",
        )

        language = st.selectbox(
            "Language",
            ["English", "Hindi", "Hinglish"],
        )

        max_characters = st.number_input(
            "Maximum Characters",
            min_value=100,
            max_value=10000,
            value=1000,
            step=50,
        )

    max_iteration = st.slider(
        "Maximum Optimization Iterations",
        min_value=1,
        max_value=10,
        value=3,
    )

    generate = st.form_submit_button(
        "Generate & Optimize",
        type="primary",
        use_container_width=True,
    )


if generate:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    if not target_audience.strip():
        st.warning("Please enter a target audience.")
        st.stop()

    initial_state = {
        "topic": topic,
        "content_type": content_type,
        "social_platform": social_platform,
        "target_audience": target_audience,
        "tone": tone,
        "language": language,
        "max_characters": int(max_characters),
        "iteration": 0,
        "max_iteration": int(max_iteration),
    }

    try:
        with st.spinner(
            "Generating, evaluating and optimizing your content..."
        ):
            result = workflow.invoke(initial_state)

        st.success("Workflow completed.")

        st.subheader("Final Content")
        st.markdown(
            result.get(
                "tweet",
                "No final content was returned.",
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Iterations",
                result.get("iteration", 0),
            )

        with col2:
            st.metric(
                "Final Evaluation",
                str(result.get("evaluation", "Not available")),
            )

        feedback = result.get("feedback")

        if feedback:
            st.subheader("Evaluator Feedback")
            st.write(feedback)

        with st.expander("View Final LangGraph State"):
            st.json(result)

    except Exception as exc:
        st.error("The workflow could not be completed.")

        with st.expander("Technical Error"):
            st.code(str(exc))