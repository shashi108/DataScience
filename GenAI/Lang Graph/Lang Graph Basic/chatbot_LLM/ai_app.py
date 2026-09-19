"""
Run with: streamlit run ai_app.py
"""

import streamlit as st
import time
from datetime import datetime
from backend import chatbot
from langchain_core.messages import HumanMessage

st.title("🤖 AI Chatbot")

# ---------- Styling ----------
st.markdown("""
<style>
    .main { background-color: #eaf4fb; }
    .header-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #0b2f5c;
        margin-bottom: 0;
    }
    .header-sub {
        color: #0b2f5c;
        font-size: 1.05rem;
        margin-top: 0.2rem;
        margin-bottom: 1.2rem;
    }
    .chat-header {
        background-color: #1f5b8f;
        color: white;
        padding: 14px 20px;
        border-radius: 14px 14px 0 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .chat-header-name { font-weight: 700; font-size: 1.1rem; margin: 0; }
    .chat-header-status { font-size: 0.85rem; color: #b7ffb7; margin: 0; }
    .chat-box {
        background-color: white;
        border-radius: 0 0 14px 14px;
        padding: 18px;
        min-height: 180px;
    }
    .bot-bubble {
        background-color: #eef1f5;
        color: #1a1a1a;
        padding: 10px 16px;
        border-radius: 14px;
        display: inline-block;
        max-width: 78%;
        margin-bottom: 4px;
    }
    .user-bubble {
        background-color: #1f5b8f;
        color: white;
        padding: 10px 16px;
        border-radius: 14px;
        display: inline-block;
        max-width: 78%;
        margin-bottom: 4px;
    }
    .avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        flex-shrink: 0;
    }
    .bot-avatar { background-color: #dce8f5; }
    .user-avatar { background-color: #1f5b8f; color: white; }
    .msg-row {
        display: flex;
        align-items: flex-end;
        gap: 8px;
        margin-bottom: 2px;
    }
    .msg-row.user { flex-direction: row-reverse; float: right; }
    .msg-row.bot { float: left; }
    .timestamp { font-size: 0.72rem; color: #888; margin: 0 6px 14px 40px; }
    .timestamp.user { text-align: right; margin: 0 40px 14px 6px; }
    .clearfix::after { content: ""; display: table; clear: both; }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<p class="header-title"> AI Chatbot</p>', unsafe_allow_html=True)


# ---------- Chat header ----------
st.markdown("""
<div class="chat-header">
    <div style="font-size:1.8rem;">🤖</div>
    <div>
        <p class="chat-header-name">AI Assistant</p>
        <p class="chat-header-status">🟢 Online</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hello! How can I help you today?","time": datetime.now().strftime("%I:%M %p")}
    ]

# ---------- Demo response logic ----------
# Define thread
thread_id = '1'
def get_bot_response(user_text: str) -> str:
    text = user_text.lower()
    # Define configuration
    config = {'configurable': {'thread_id': thread_id}}
    # Invoke chatbot
    response = chatbot.invoke( {'messages': [HumanMessage(content=text)]},config=config)
    # Get AI response
    ai_message = response['messages'][-1].content
    return ai_message
# ---------- Render chat ----------
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            st.markdown(f"""
            <div class="clearfix">
                <div class="msg-row bot">
                    <div class="avatar bot-avatar">🤖</div>
                    <div class="bot-bubble">{msg['text']}</div>
                </div>
                <div class="timestamp">{msg['time']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="clearfix">
                <div class="msg-row user">
                    <div class="avatar user-avatar">🧑</div>
                    <div class="user-bubble">{msg['text']}</div>
                </div>
                <div class="timestamp user">{msg['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Input ----------
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", label_visibility="collapsed", placeholder="Type your message...")
    with col2:
        submitted = st.form_submit_button("➤")

if submitted and user_input.strip():
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "text": user_input, "time": now})
    with st.spinner("Thinking..."):
        time.sleep(0.4)
        reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "bot", "text": reply, "time": now})
    st.rerun()

# ---------- Tech stack footer ----------
st.markdown("---")
st.markdown("**Tech Stack (for this project)**")
c1, c2, c3, c4 = st.columns(4)
c1.markdown("🐍 **Lang Graph**")
c2.markdown("🎈 **Streamlit**")
c3.markdown("💬 **Session State**")
c4.markdown("🔌 **LLM API**")
st.markdown(
    """
    <div class="footer">
        © 2026 · AI Chatbot · Developed by <strong>Shashi Kumar</strong>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: #888;
        padding: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)