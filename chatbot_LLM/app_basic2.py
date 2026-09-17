import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 900px;
    }

    /* User message - RIGHT */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 10px 0;
    }

    .user-bubble {
        background-color: #DCF8C6;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        color: black;
        font-size: 16px;
    }

    /* AI message - LEFT */
    .ai-message {
        display: flex;
        justify-content: flex-start;
        margin: 10px 0;
    }

    .ai-bubble {
        background-color: #F1F1F1;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        color: black;
        font-size: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# TITLE
# ==================================================

st.title("💬 AI Chatbot")
st.caption("Ask me anything...")


# ==================================================
# SESSION STATE
# ==================================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state["message_history"]:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <div class="user-bubble">
                    👤 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-message">
                <div class="ai-bubble">
                    🤖 {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# CHAT INPUT
# ==================================================

user_input = st.chat_input("Type your message here...")


# ==================================================
# THREAD ID
# ==================================================

thread_id = "1"


# ==================================================
# PROCESS USER MESSAGE
# ==================================================

if user_input:

    # ----------------------------------------------
    # Save user message
    # ----------------------------------------------

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ----------------------------------------------
    # Display user message - RIGHT
    # ----------------------------------------------

    st.markdown(
        f"""
        <div class="user-message">
            <div class="user-bubble">
                👤 {user_input}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # Configuration
    # ----------------------------------------------

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }


    # ----------------------------------------------
    # Invoke chatbot
    # ----------------------------------------------

    response = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        },
        config=config
    )


    # ----------------------------------------------
    # Get AI response
    # ----------------------------------------------

    ai_message = response["messages"][-1].content


    # ----------------------------------------------
    # Save AI response
    # ----------------------------------------------

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )


    # ----------------------------------------------
    # Display AI response - LEFT
    # ----------------------------------------------

    st.markdown(
        f"""
        <div class="ai-message">
            <div class="ai-bubble">
                🤖 {ai_message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

