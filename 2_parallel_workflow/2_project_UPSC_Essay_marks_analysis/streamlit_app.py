import streamlit as st

from pipeline import workflow


st.set_page_config(
    page_title="UPSC Essay Evaluator",
    page_icon="📝",
    layout="centered",
)

st.title("📝 UPSC Essay Evaluator")
st.caption(
    "AI-powered essay evaluation using a parallel LangGraph workflow."
)

st.markdown(
    """
The essay is evaluated independently for:

- **Language quality**
- **Clarity / thought quality**
- **Depth of analysis**

The results are then combined into a final summary and average score.
"""
)

uploaded_file = st.file_uploader(
    "Upload a TXT essay",
    type=["txt"],
)

typed_essay = st.text_area(
    "Or paste your essay here",
    height=320,
    placeholder="Paste your UPSC essay here...",
)

essay_text = typed_essay

if uploaded_file is not None:
    try:
        essay_text = uploaded_file.read().decode("utf-8")
        st.success("Essay loaded successfully.")
    except UnicodeDecodeError:
        st.error("The uploaded file could not be decoded as UTF-8 text.")
        essay_text = ""

evaluate = st.button(
    "Evaluate Essay",
    type="primary",
    use_container_width=True,
)

if evaluate:
    if not essay_text.strip():
        st.warning("Please upload or paste an essay first.")
        st.stop()

    try:
        with st.spinner("Evaluating essay..."):
            result = workflow.invoke(
                {
                    "essay": essay_text
                }
            )

        overall_feedback = result.get(
            "overall_feedback",
            "No overall feedback was returned."
        )

        avg_score = result.get("avg_score")
        individual_scores = result.get("individual_score", [])

        lang_feedback = result.get(
            "lang_feedback",
            "No language feedback was returned."
        )
        clarity_feedback = result.get(
            "clarity_feedback",
            "No clarity feedback was returned."
        )
        analysis_feedback = result.get(
            "analysis_feedback",
            "No analysis feedback was returned."
        )

        st.success("Evaluation completed.")

        st.subheader("Final Result")

        if avg_score is not None:
            st.metric(
                "Average Score",
                f"{float(avg_score):.2f} / 10",
            )

        st.markdown("### Summary Feedback")
        st.write(overall_feedback)

        if individual_scores:
            st.markdown("### Individual Scores")

            cols = st.columns(len(individual_scores))

            for index, score in enumerate(individual_scores):
                with cols[index]:
                    st.metric(
                        f"Evaluator {index + 1}",
                        f"{score} / 10",
                    )

            st.caption(
                "The scores are collected from parallel evaluator nodes. "
                "They are shown generically because the current state stores them "
                "in one merged list rather than separate named score fields."
            )

        st.markdown("### Detailed Feedback")

        with st.expander("Language Feedback", expanded=True):
            st.write(lang_feedback)

        with st.expander("Clarity / Thought Feedback"):
            st.write(clarity_feedback)

        with st.expander("Analysis Feedback"):
            st.write(analysis_feedback)

        st.divider()

        with st.expander("Raw LangGraph Result"):
            st.json(result)

    except Exception as exc:
        st.error(
            "The evaluation could not be completed. "
            "This may be caused by the LLM provider or backend."
        )

        with st.expander("Technical Error"):
            st.code(str(exc))