# ----------------------------------------------------------------
"""
# Using SQLite Checkpointer in LangGraph

### Step 1: Import `SqliteSaver`
Replace the in-memory checkpointer:
from langgraph.checkpoint.memory import MemorySaver
with the SQLite-based checkpointer:
from langgraph.checkpoint.sqlite import SqliteSaver
---

### Step 2: Install the SQLite Checkpoint Package
Run the following command in the terminal:

```bash
pip install langgraph-checkpoint-sqlite
```
---
### Step 3: Import SQLite
Add the Python SQLite library:
```python
import sqlite3
```
---
### Step 4: Create the SQLite Database
Create a database connection:
```python
conn = sqlite3.connect(
    database="chatbot.db",
    check_same_thread=False
)
```
Here:

* `chatbot.db` → SQLite database file where the checkpoint data will be stored.
* `check_same_thread=False` → Allows the SQLite connection to be used across different threads.

> **Note:** SQLite connections are thread-sensitive by default. 
Setting `check_same_thread=False` disables that restriction, which can be useful when the application needs to access the connection from multiple threads. It does not by itself make all concurrent database operations safe; proper connection/concurrency handling is still important.
---
### Step 5: Replace `MemorySaver` with `SqliteSaver`
Previously, we used:
```python
checkpointer = MemorySaver()
```
Replace it with:

```python
checkpointer = SqliteSaver(conn=conn)
```
"""
# ---------------- Import Libraries ----------------
#Define Library
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
#Saving data in memory
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
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
conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
chatbot=graph.compile(checkpointer=checkpointer)

#define thread
# thread_id='2'
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