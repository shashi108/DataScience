
#%%%%%%%%% LangSmith >> Prompt >> LLM>>
#Ollama: Helpful to intract with LLM model
#ChatPromptTemplate:It allows developers to define templates that can dynamically incorporate user inputs and generate structured responses
#StrOutputParser:Display output response from LLM into a string formatf

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama


import streamlit as st

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## streamlit framework
st.title('Langchain Demo With LLAMA2 API')
input_text=st.text_input("Search the topic you want")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ollama LLAma2 LLm 
llm=Ollama(model="deepseek-r1:7b")
output_parser=StrOutputParser()
#%%%%%%%%%% create chain %%%%%%%%%%%%%%%%%%%%%
chain=prompt|llm|output_parser
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if input_text:
    st.write(chain.invoke({"question":input_text}))
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% streamlit run app.py %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%