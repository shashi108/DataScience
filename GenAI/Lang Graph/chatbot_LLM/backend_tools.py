# ============================================================
# 1. Imports
# ============================================================
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage

from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import requests
import sqlite3
#============================================================
# 2. Load Environment Variables
# ============================================================
# ============================================================
# 3. LLM
# ============================================================
llm =ChatOllama(model="qwen3:4b")
# ============================================================
# 4. Tools
# ============================================================

# ------------------------------------------------------------
# Tool 1: DuckDuckGo Search
# ------------------------------------------------------------
search_tool = DuckDuckGoSearchRun(region="us-en")
# ------------------------------------------------------------
# Tool 2: Calculator
# ------------------------------------------------------------

@tool
def calculator(first_num: float,second_num: float,operation: str) -> dict:
    """
    Perform a basic arithmetic operation.

    Supported operations:
    - add
    - sub
    - mul
    - div
    """

    try:

        if operation == "add":
            result = first_num + second_num

        elif operation == "sub":
            result = first_num - second_num

        elif operation == "mul":
            result = first_num * second_num

        elif operation == "div":

            if second_num == 0:
                return {
                    "error": "Division by zero is not allowed"
                }

            result = first_num / second_num

        else:
            return {
                "error": f"Unsupported operation: {operation}"
            }

        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ------------------------------------------------------------
# Tool 3: Stock Price
# -----------------------------------------------------------
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()

# ============================================================
# 5. Register Tools
# ============================================================

tools = [search_tool,get_stock_price,calculator]
# ============================================================
# 6. Bind Tools to LLM
# ============================================================
llm_with_tools = llm.bind_tools(tools)
# ============================================================
# 7. State
# ============================================================
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
# ============================================================
# 8. Chat Node
# ============================================================
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}
# ============================================================
# 9. Tool Node
# ============================================================
tool_node = ToolNode(tools)
# ============================================================
# 10. SQLite Checkpointer
# ============================================================
conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
# ============================================================
# 11. Create LangGraph
# ============================================================
graph = StateGraph(ChatState)
# Add nodes
graph.add_node( "chat_node",chat_node)
graph.add_node("tools",tool_node)
# ============================================================
# 12. Define Edges
# ============================================================
# START → chat_node
graph.add_edge(START,"chat_node")

# chat_node → tools OR END
graph.add_conditional_edges( "chat_node",tools_condition)

# tools → chat_node
graph.add_edge("tools","chat_node")

# ============================================================
# 13. Compile Graph
# ============================================================
chatbot = graph.compile(checkpointer=checkpointer)
# ============================================================
# 14. Retrieve All Threads
# ============================================================

def retrieve_all_threads():

    all_threads = set()

    for checkpoint in checkpointer.list(None):

        thread_id = (
            checkpoint.config["configurable"]["thread_id"]
        )

        all_threads.add(thread_id)

    return list(all_threads)


# ============================================================
# 15. Helper Function
# ============================================================

def chat(user_message: str,thread_id: str = "default"):
    """
    Send a message to the LangGraph chatbot.
    """
    config = {"configurable": {"thread_id": thread_id}}
    response = chatbot.invoke({"messages": [HumanMessage(content=user_message)]},config=config)
    return response

# ============================================================
# 16. Example Usage
# ============================================================
# 
# if __name__ == "__main__":
    # thread_id = "user_1"
    # response = chat( "What is 50 multiplied by 20?",thread_id)
    # print("\n==============================")
    # print("Assistant Response")
    # print("==============================\n")
    # print(response["messages"][-1].content) 
    
    
    
     