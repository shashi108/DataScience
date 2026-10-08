#-------------- Import Library -----------------------------------
import streamlit as st
from backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage
#----------------------------------------------------------
st.title("💬 AI Chatbot")
# This will not reset the value of message_history
# on every new message.
# st.session_state is used to maintain data between Streamlit reruns.
#----------------------------------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# Display previous messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
#----------------------------------------------------------
# Get user input
user_input = st.chat_input("Type here")
# Define thread
thread_id = '1'
if user_input:

    # Save user message in session state
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    # Display user message
    with st.chat_message('user'):
        st.text(user_input)

    # Define configuration
    config = {'configurable': {'thread_id': thread_id}}

    # Invoke chatbot
    response = chatbot.invoke( {'messages': [HumanMessage(content=user_input)]},config=config)
    # Get AI response
    ai_message = response['messages'][-1].content

    # Save AI message
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    # Display AI response
    with st.chat_message('assistant'):
        st.text(ai_message)