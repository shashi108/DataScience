#----------------------------------------------------------------
'''
What is streaming
In LLM ,streaming means the model starts sending words as soon as they are generated,instead of waiting for the entire 
response to be ready before returning it.
'''
#-------------- Import Library -----------------------------------
import streamlit as st
from backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage
#----------------------------------------------------------
st.title("💬 AI Chatbot")
# This will not reset the value of message_history
# on every new message.
# st.session_state is used to maintain data between Streamlit reruns.
#------------------------stream session ----------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# Display previous messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



# Define configuration
thread_id = '1'
config = {'configurable': {'thread_id': thread_id}}
#----------------------------------------------------------
# Get user input
user_input = st.chat_input("Type here")
# Define thread

if user_input:

    # Save user message in session state
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    # Display user message
    with st.chat_message('user'):
        st.text(user_input)



    # Invoke chatbot
    #response = chatbot.invoke( {'messages': [HumanMessage(content=user_input)]},config=config)
    #stram response
    with st.chat_message('assistant'):
     ai_message=st.write_stream(
       message_chunk.content for message_chunk, metadeta in chatbot.stream( 
        {'messages': [HumanMessage(content=user_input)]},
        config=config,
        stream_mode='messages'
      )
    )

    # Save AI message
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
