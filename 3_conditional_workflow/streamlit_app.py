import streamlit as st
import uuid

from langgraph.types import Command
from pipeline import workflow


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DSA Practice Agent",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 DSA Practice Agent")

st.caption(
    "Practice DSA questions with Easy, Medium and Tough difficulty."
)


# =========================================================
# SESSION STATE
# =========================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "result" not in st.session_state:
    st.session_state.result = None

if "started" not in st.session_state:
    st.session_state.started = False


# =========================================================
# CONFIG FOR LANGGRAPH MEMORY
# =========================================================

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}


# =========================================================
# START NEW PRACTICE
# =========================================================

if not st.session_state.started:

    st.subheader("Start Practice")

    topic = st.text_input(
        "Enter DSA Topic",
        placeholder="Example: Arrays, Hashing, Strings, Sliding Window"
    )

    difficulty = st.selectbox(
        "Select Difficulty",
        [
            "Easy",
            "Medium",
            "Tough"
        ]
    )

    if st.button(
        "Generate Question",
        type="primary",
        use_container_width=True
    ):

        if not topic.strip():

            st.warning(
                "Please enter a DSA topic."
            )

        else:

            try:

                with st.spinner(
                    "Generating your question..."
                ):

                    result = workflow.invoke(
                        {
                            "topic": topic,
                            "difficulty": difficulty.lower(),
                            "attempts": 0
                        },
                        config=config
                    )

                st.session_state.result = result
                st.session_state.started = True

                st.rerun()

            except Exception as e:

                st.error(
                    "Unable to generate question."
                )

                with st.expander(
                    "Technical Error"
                ):
                    st.code(str(e))


# =========================================================
# ACTIVE PRACTICE SESSION
# =========================================================

else:

    result = st.session_state.result


    # =====================================================
    # GRAPH IS WAITING FOR USER ANSWER
    # =====================================================

    if result and "__interrupt__" in result:

        interrupt_data = (
            result["__interrupt__"][0].value
        )

        question = interrupt_data.get(
            "question",
            result.get(
                "question",
                "Question unavailable"
            )
        )

        attempt = interrupt_data.get(
            "attempt",
            result.get(
                "attempts",
                0
            ) + 1
        )


        # -------------------------------------------------
        # QUESTION
        # -------------------------------------------------

        st.subheader("💻 Your Question")

        st.markdown(question)

        st.divider()


        # -------------------------------------------------
        # PREVIOUS WRONG ATTEMPT FEEDBACK
        # -------------------------------------------------

        if result.get("response"):

            st.warning(
                f"Attempt {result.get('attempts', 0)} Feedback"
            )

            st.write(
                result["response"]
            )


        # -------------------------------------------------
        # ATTEMPT INFO
        # -------------------------------------------------

        st.caption(
            f"Current Attempt: {attempt} / 3"
        )


        # -------------------------------------------------
        # ANSWER INPUT
        # -------------------------------------------------

        with st.form(
            key=f"answer_form_{attempt}"
        ):

            user_answer = st.text_area(
                "Write your solution",
                height=300,
                placeholder="""Example:

def solution(nums):
    # write your code here
    return ...
"""
            )

            submit_answer = st.form_submit_button(
                "Submit Answer",
                type="primary",
                use_container_width=True
            )


        # -------------------------------------------------
        # RESUME LANGGRAPH
        # -------------------------------------------------

        if submit_answer:

            if not user_answer.strip():

                st.warning(
                    "Please write your solution first."
                )

            else:

                try:

                    with st.spinner(
                        "Analyzing your solution..."
                    ):

                        result = workflow.invoke(
                            Command(
                                resume=user_answer
                            ),
                            config=config
                        )

                    st.session_state.result = result

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Something went wrong while analyzing your answer."
                    )

                    with st.expander(
                        "Technical Error"
                    ):
                        st.code(str(e))


    # =====================================================
    # GRAPH FINISHED
    # =====================================================

    elif result:

        st.subheader("📊 Final Result")


        # -------------------------------------------------
        # CORRECT ANSWER
        # -------------------------------------------------

        if result.get("is_correct") is True:

            st.success(
                "🎉 Correct Answer!"
            )

            if result.get("response"):

                st.write(
                    result["response"]
                )


        # -------------------------------------------------
        # FAILED AFTER MAX ATTEMPTS
        # -------------------------------------------------

        else:

            st.error(
                "Maximum attempts reached."
            )

            st.markdown(
                "### 📚 Solution & Explanation"
            )

            if result.get("response"):

                st.write(
                    result["response"]
                )


        # -------------------------------------------------
        # EXTRA INFORMATION
        # -------------------------------------------------

        with st.expander(
            "View Final State"
        ):

            st.json(result)


        st.divider()


        # -------------------------------------------------
        # NEW PRACTICE SESSION
        # -------------------------------------------------

        if st.button(
            "🔄 Practice Another Question",
            use_container_width=True
        ):

            st.session_state.thread_id = str(
                uuid.uuid4()
            )

            st.session_state.result = None

            st.session_state.started = False

            st.rerun()