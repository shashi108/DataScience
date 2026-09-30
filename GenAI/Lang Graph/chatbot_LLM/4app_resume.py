# ----------------------------------------------------------------
"""
Chat History & Thread Management

1. Create Sidebar
   - Add sidebar title
   - Add New Chat button
   - Add My Conversations section

2. Generate Thread ID
   - Generate a unique thread_id
   - Store it in st.session_state
   - Display current thread ID

3. When New Chat is clicked:
   - Generate a new thread_id
   - Save it in session state
   - Reset message history
   - Start a fresh conversation

4. Store Thread IDs
   - Maintain a list of all conversation/thread IDs

5. Display Conversations
   - Display stored thread IDs as clickable buttons

6. When a thread is selected:
   - Set it as the active thread
   - Load its saved conversation/checkpoint
   - Display previous messages
   - Continue conversation
"""

# ---------------- Import Libraries ----------------

import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid


# ---------------- Utility Functions ----------------

def generate_thread_id():
    """Generate a unique thread ID."""
    return str(uuid.uuid4())


def add_thread(thread_id):
    """Add thread ID to chat_threads if it does not already exist."""
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    """Create a new chat thread."""
    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

    add_thread(thread_id)


def load_conversation(thread_id):
    """Load messages saved in the LangGraph checkpoint."""
    
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = chatbot.get_state(config=config)

    return state.values.get("messages", [])


def convert_messages(messages):
    """Convert LangChain messages into Streamlit message format."""

    temp_messages = []

    for msg in messages:

        if isinstance(msg, HumanMessage):
            role = "user"
        else:
            role = "assistant"

        temp_messages.append(
            {
                "role": role,
                "content": msg.content
            }
        )

    return temp_messages


# ---------------- Session State Initialization ----------------

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []


# Add current thread to thread list
add_thread(st.session_state["thread_id"])


# ---------------- Sidebar UI ----------------

st.sidebar.title("🤖 AI Chatbot")


# New Chat button
if st.sidebar.button("➕ New Chat"):

    reset_chat()

    # Rerun so the new empty chat is displayed immediately
    st.rerun()


st.sidebar.header("💬 My Conversations")


# Display all threads
for thread_id in st.session_state["chat_threads"][::-1]:

    if st.sidebar.button(
        thread_id,
        key=f"thread_{thread_id}"
    ):

        # Make selected thread active
        st.session_state["thread_id"] = thread_id

        # Load saved conversation
        messages = load_conversation(thread_id)

        # Convert LangChain messages to Streamlit format
        st.session_state["message_history"] = convert_messages(messages)

        # Rerun to display selected conversation
        st.rerun()


# Display current thread ID
st.sidebar.markdown("---")
st.sidebar.caption("Current Thread")
st.sidebar.code(st.session_state["thread_id"])


# ---------------- Main UI ----------------

st.title("💬 AI Chatbot")


# Display previous messages
for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------- Current Thread Config ----------------

# IMPORTANT:
# Create config AFTER the thread selection logic.
config = {
    "configurable": {
        "thread_id": st.session_state["thread_id"]
    }
}


# ---------------- Chat Input ----------------

user_input = st.chat_input("Type here...")


if user_input:

    # ---------------- Save User Message ----------------

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ---------------- Display User Message ----------------

    with st.chat_message("user"):
        st.write(user_input)


    # ---------------- Invoke / Stream Chatbot ----------------

    with st.chat_message("assistant"):

        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata
            in chatbot.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config,
                stream_mode="messages"
            )
        )


    # ---------------- Save AI Message ----------------

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )
    
# ---------------- Footer ----------------

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 32px;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 11px;
        color: #888;

        background: rgba(255, 255, 255, 0.95);
        border-top: 1px solid #e5e5e5;

        z-index: 999999;
    }
    </style>

    <div class="footer">
        © 2026 · AI Chatbot · Developed by <strong>&nbsp;Shashi Kumar</strong>
    </div>
    """,
    unsafe_allow_html=True
)