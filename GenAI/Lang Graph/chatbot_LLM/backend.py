#Define Library
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
#Saving data in memory
from langgraph.checkpoint.memory import MemorySaver

##########local ollama
from langchain_ollama import ChatOllama
model = ChatOllama(model="gemma3:4b")
response = model.invoke("the capital of India? in one word")
#print(response.content)

#Define State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

##
def chat_node(state : ChatState):
    #take a query from state
    message=state['messages']

    #Send to LLM
    response=model.invoke(message)

    #response store state
    return{'messages':[response]}

#define graph ,node and edges
graph=StateGraph(ChatState)

#node
graph.add_node('chat_node',chat_node)

#edge
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

#create checkpoint for data saving
checkpointer = MemorySaver()
chatbot=graph.compile(checkpointer=checkpointer)

#define thread
# thread_id='1'
# while True:
    # user_message=input('Type here : ')
    # print('User :',user_message)
    # if user_message.strip().lower() in ['exit','quit','bye']:
    #    break   
# 
    # config= {'configurable' :{'thread_id':thread_id}}
    #response=workflow.invoke({'messages':[HumanMessage(content=user_message)]})
    # response=chatbot.invoke({'messages':[HumanMessage(content=user_message)]},config=config)
    # print('AI :' ,response['messages'][-1].content)