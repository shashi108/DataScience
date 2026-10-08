# AI Chatbot with LangGraph and Ollama

This project demonstrates how to build a simple chatbot using Python, Streamlit, LangGraph, and a local Ollama model. It includes multiple UI variations that show different ways of integrating a LangGraph backend with various features like persistent storage, tool calling, and streaming responses.

## 🎯 Project Purpose

The project is designed to teach and demonstrate:

- How to build a chatbot backend with LangGraph
- How to connect a model using LangChain and Ollama
- How to manage chat state with memory checkpoints
- How to build different Streamlit chat interfaces
- How to stream responses and manage conversation threads
- How to implement stateful conversations with message history
- How to create multiple UI variants for different use cases
- How to persist conversation data using SQLite
- How to integrate external tools and enable agent capabilities

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web-based UI framework
- **LangGraph** - Graph-based workflow orchestration
- **LangChain Core** - AI/LLM framework components
- **LangChain Ollama** - Integration with local Ollama models
- **Ollama** - Local LLM runtime (privacy-first, no API calls)
- **SQLite** - Persistent checkpoint storage
- **DuckDuckGo Search** - Web search integration for tools

## 📁 Project Structure

```text
chatbot_LLM/
├── backend.py                # LangGraph chatbot graph and model setup
├── backend_sqlite.py         # SQLite-based persistent checkpoint storage
├── backend_tools.py          # LangGraph with tool integration and agent capabilities
├── ai_app.py                 # Main styled Streamlit chat application
├── 1app_basic.py             # Basic Streamlit chat app (minimal UI)
├── 2app_basic.py             # Chat app with custom CSS styling
├── 3app_stream.py            # Streaming response example
├── 4app_resume.py            # Chat history + thread management example
├── 5app_sqlite.py            # SQLite persistent conversations with thread switching
├── 6app_tools.py             # Agent chatbot with tool calling capabilities
├── chatbot.db                # SQLite database (auto-created)
└── README.md                 # Project documentation
```

## 📋 Prerequisites

Before running the project, make sure you have:

- **Python 3.9+** - Latest Python version recommended
- **pip** - Python package manager
- **Ollama** - Installed and running locally ([Download here](https://ollama.ai))
- A compatible model downloaded locally (e.g., Gemma, Llama2, Mistral, Qwen)

### Install Ollama and Download a Model

```bash
# Download and install Ollama from https://ollama.ai
# Then pull a model (example with Gemma 3)
ollama pull gemma3:4b

# Or pull Qwen for tool-calling examples
ollama pull qwen3:4b
```

### Install Python Dependencies

```bash
pip install streamlit langgraph langchain-core langchain-ollama langgraph-checkpoint-sqlite langchain-community
```

Or install from a requirements file (if available):

```bash
pip install -r requirements.txt
```

## 🚀 How It Works

### Backend Architecture (`backend.py`)

`backend.py` defines a LangGraph workflow that orchestrates the chatbot:

- **ChatState** - Data structure storing conversation messages
- **add_messages** - Function that merges new messages with chat history
- **chat_node()** - Core node that sends messages to the LLM and processes responses
- **MemorySaver** - Persistent state manager for the active session
- **ChatOllama** - Integration with local Ollama model (e.g., "gemma3:4b")

The workflow follows this pattern:
1. User input → LangGraph node
2. Node processes message and maintains state
3. State passed to LLM via LangChain Ollama
4. Response generated and added to state
5. Updated state returned to UI

### SQLite Persistence (`backend_sqlite.py`)

`backend_sqlite.py` extends the basic backend with persistent checkpoint storage:

- **SqliteSaver** - Replaces MemorySaver for database-backed persistence
- **chatbot.db** - SQLite database file storing all conversation checkpoints
- **Thread Management** - Retrieve saved conversations by thread ID
- **Cross-Session Recovery** - Conversations persist even after app restarts

Key differences from basic backend:
```python
# Instead of in-memory storage:
checkpointer = MemorySaver()

# Use SQLite for persistence:
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
```

### Agent with Tool Integration (`backend_tools.py`)

`backend_tools.py` demonstrates LangGraph's agent capabilities with external tool integration:

- **Tool Binding** - LLM can invoke external tools when needed
- **DuckDuckGo Search** - Web search integration for information retrieval
- **Calculator Tool** - Arithmetic operations (add, subtract, multiply, divide)
- **Stock Price Tool** - Real-time stock price lookups via Alpha Vantage API
- **Conditional Routing** - Intelligent routing between chat and tool nodes
- **Tool Node** - Executes requested tools and returns results to LLM

Tool integration flow:
1. User asks a question requiring external information
2. LLM decides which tool(s) to use
3. Tool Node executes the tool
4. Results returned to LLM for processing
5. LLM formulates final response based on tool output

### UI Examples

The project includes several front-end implementations:

| App | File | Features | Use Case |
|-----|------|----------|----------|
| **Main App** | `ai_app.py` | Styled interface, session state, message formatting | Production demo |
| **Basic** | `1app_basic.py` | Minimal UI, simple message display | Learning basics |
| **Styled** | `2app_basic.py` | Custom CSS styling, better UX | Development reference |
| **Streaming** | `3app_stream.py` | Real-time response streaming | Advanced streaming patterns |
| **Threaded** | `4app_resume.py` | Chat history, thread management, conversation recovery | Multi-session handling |
| **SQLite** | `5app_sqlite.py` | Persistent conversations, thread switching, database recovery | Production-grade persistence |
| **Agent Tools** | `6app_tools.py` | Tool calling, external integrations, agent decision-making | Extended capabilities |

## 🏃 Running the App

### Prerequisites Check

Before running, ensure Ollama is running:

```bash
ollama serve
```

(In another terminal, proceed with the commands below)

### Navigate to Project Directory

```bash
cd "GenAI/Lang Graph/chatbot_LLM"
```

### Run the Main Styled App (Recommended)

```bash
streamlit run ai_app.py
```

This will launch the main chatbot interface at `http://localhost:8501`

### Run Alternative Versions

**Basic App:**
```bash
streamlit run 1app_basic.py
```

**Styled Basic App:**
```bash
streamlit run 2app_basic.py
```

**Streaming Response App:**
```bash
streamlit run 3app_stream.py
```

**Chat History & Thread Management:**
```bash
streamlit run 4app_resume.py
```

**SQLite Persistent Conversations:**
```bash
streamlit run 5app_sqlite.py
```

**Agent Chatbot with Tools:**
```bash
streamlit run 6app_tools.py
```

## 📊 Example Workflow

### Basic Chat Flow
1. **Start Ollama** - Ensure Ollama service is running locally
2. **Launch Streamlit App** - Run one of the app commands above
3. **Enter Prompt** - Type a message in the chat input box
4. **Backend Processing** - Message sent to LangGraph backend
5. **LLM Inference** - Backend calls local Ollama model
6. **Response Generation** - LLM processes and generates answer
7. **Display Result** - Response displayed in UI with message history
8. **Maintain State** - Conversation history retained for context

Example conversation flow:
```
User: "What is machine learning?"
LLM Response: "Machine learning is a subset of AI that..."

User: "Can you give me an example?"
LLM Response: "Sure! For example, email spam filters use..."
```

### SQLite Persistence Flow (5app_sqlite.py)
1. User sends message → Processed by LangGraph
2. Response generated and saved to SQLite database
3. Conversation thread ID associated with checkpoint
4. User can start new chat → Creates new thread
5. Click existing conversation → Loads messages from SQLite
6. App restart → All conversations still available (recovery!)

### Agent Tool Flow (6app_tools.py)
1. **User Query** - "What's the stock price of AAPL?"
2. **LLM Decision** - Determines `get_stock_price` tool is needed
3. **Tool Execution** - Calculator/Search/Stock tool invoked
4. **Result Processing** - Tool output returned to LLM
5. **Response Generation** - LLM formulates answer with tool data
6. **Display** - Final response shown to user with context

Example agent conversation:
```
User: "Calculate 50 times 20"
Agent: Uses calculator tool → Result: 1000

User: "Search for Python tutorials"
Agent: Uses DuckDuckGo search tool → Returns relevant results

User: "What's Tesla's stock price?"
Agent: Uses stock price tool → Returns current TSLA price
```

## 🔑 Key Features

✅ **Local Processing** - No data sent to external APIs (privacy-first)  
✅ **Stateful Conversations** - Context maintained across messages  
✅ **Multiple UI Patterns** - Examples for different use cases  
✅ **Streaming Support** - Real-time response generation  
✅ **Thread Management** - Handle multiple conversation threads  
✅ **Easy Model Switching** - Change models by updating model name  
✅ **Extensible Architecture** - Easy to add tools, RAG, or other features  
✅ **Persistent Storage** - SQLite-backed conversation history  
✅ **Agent Capabilities** - Tool calling and external integrations  
✅ **Cross-Session Recovery** - Restore conversations after restart  

## 📝 Detailed Feature Explanations

### 5. SQLite Persistent Conversations (5app_sqlite.py)

**What it does:**
- Stores all conversations in a SQLite database (`chatbot.db`)
- Allows switching between multiple conversation threads
- Recovers all previous conversations even after app restart
- Displays list of all past conversations in sidebar

**Key Components:**
```python
# Database setup
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# Load existing threads from database
all_thread = set()
for checkpoint in checkpointer.list(None):
    all_thread.add(checkpoint.config['configurable']['thread_id'])

# Retrieve full conversation history
state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
messages = state.values.get("messages", [])
```

**Features:**
- ➕ **New Chat** - Create fresh conversation thread
- 💬 **My Conversations** - Browse and switch between saved threads
- 📝 **Full History** - All messages preserved in database
- 🔄 **Recovery** - Restore conversations after app crashes or restarts

**Use Cases:**
- Multi-user support with independent conversation histories
- Long-running projects with persistent context
- Audit trails and conversation logging
- Building a personal AI assistant with memory across sessions

---

### 6. Agent Chatbot with Tools (6app_tools.py)

**What it does:**
- Extends the chatbot with external tool capabilities
- LLM can intelligently decide when and which tools to use
- Three main tools: Search, Calculator, Stock Price lookup
- Demonstrates advanced LangGraph patterns with conditional routing

**Supported Tools:**

1. **DuckDuckGo Search** - Web search for information
   ```
   User: "What's the capital of France?"
   Agent: Searches for answer → Returns: "Paris"
   ```

2. **Calculator** - Basic arithmetic operations
   ```
   User: "What's 50 * 20?"
   Agent: Calls calculator tool → Returns: 1000
   Supported: add, sub, mul, div
   ```

3. **Stock Price Lookup** - Real-time stock data
   ```
   User: "What's AAPL stock price?"
   Agent: Fetches from Alpha Vantage API → Returns current price
   ```

**Architecture:**
```python
# Tool binding to LLM
tools = [search_tool, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)

# Conditional routing
graph.add_conditional_edges("chat_node", tools_condition)
# Routes to tool_node if tools needed, else to END

# Tool execution
tool_node = ToolNode(tools)
graph.add_edge("tools", "chat_node")  # Results back to LLM
```

**Decision Flow:**
```
User Input
    ↓
chat_node (LLM evaluation)
    ↓
[Tools needed?]
    ├─ YES → tool_node (execute tools)
    │         ↓
    │         chat_node (process results)
    │         ↓
    │         END
    │
    └─ NO → END (direct response)
```

**Configuration:**
- Model: `qwen3:4b` (better tool calling than gemma)
- Search region: US English
- Stock API: Alpha Vantage (requires API key in code)

**Use Cases:**
- Real-time information retrieval (news, weather, stock prices)
- Complex calculations and data processing
- Research assistant with web search
- Financial advisor with market data
- General-purpose AI agent with extended capabilities

---

## 🔧 Customization Guide

### Change the LLM Model

Edit `backend.py` or respective backend file and modify the model name:

```python
# Current
model = ChatOllama(model="gemma3:4b")

# Change to different model
model = ChatOllama(model="llama2")  # or mistral, neural-chat, qwen3, etc.

# For tool-calling, use:
model = ChatOllama(model="qwen3:4b")  # Better tool support
```

### Modify System Prompt

Add custom system instructions to backend files:

```python
system_prompt = """You are a helpful AI assistant specializing in data science and AI topics."""
```

### Add New Tools (6app_tools.py)

```python
from langchain_core.tools import tool

@tool
def my_new_tool(param1: str, param2: int) -> str:
    """Tool description for the LLM"""
    # Implementation here
    return result

# Add to tools list
tools = [search_tool, get_stock_price, calculator, my_new_tool]
llm_with_tools = llm.bind_tools(tools)
```

### Add Custom CSS Styling

Modify the Streamlit theme in any app file:

```python
st.set_page_config(page_title="AI Chatbot", layout="wide")
```

### Configure SQLite Database Location (5app_sqlite.py)

```python
# Change database file location
conn = sqlite3.connect(database='path/to/custom_chatbot.db', check_same_thread=False)
```

## 📝 Notes

- **Demo Project** - This is a learning/demo project rather than production-ready
- **Memory Limitation** - In-memory models reset on app restart (5app_sqlite.py & 6app_tools.py persist)
- **Model Download** - Models are downloaded to Ollama cache on first run (may take time)
- **GPU Support** - Ollama can leverage GPU if available for faster inference
- **Tool API Keys** - Stock price tool requires Alpha Vantage API key (free tier available)
- **SQLite Concurrency** - `check_same_thread=False` allows multi-threaded access but not full concurrency
- **Production Use** - For real-world deployment, add authentication, error handling, logging, and monitoring

## 🚀 Production Considerations

For deploying this chatbot to production, consider:

1. **Persistence** - Use database (PostgreSQL, MongoDB) for multi-user support
2. **Authentication** - Add user authentication and authorization
3. **Error Handling** - Comprehensive error handling and recovery
4. **Logging** - Implement logging for debugging and monitoring
5. **RAG Integration** - Add Retrieval Augmented Generation for knowledge bases
6. **Tool Calling** - Enable advanced agent capabilities with custom tools
7. **Load Testing** - Test under high concurrent user loads
8. **Docker** - Containerize for easy deployment
9. **Environment Variables** - Use .env files for configuration and API keys
10. **API Rate Limiting** - Implement rate limiting for stability
11. **Database Migration** - Plan for conversation data migration strategies
12. **Monitoring** - Add metrics and alerts for production usage

## 📚 Learning Path

1. **Start** → Run `1app_basic.py` to understand basic structure
2. **Explore** → Try `2app_basic.py` for styled UI patterns
3. **Advanced** → Run `3app_stream.py` for streaming concepts
4. **Expert** → Use `4app_resume.py` to manage state across sessions
5. **Persistent** → Run `5app_sqlite.py` for database-backed conversations
6. **Agent** → Launch `6app_tools.py` for tool integration and agent patterns
7. **Production** → Customize `ai_app.py` for your use case

## 🤝 Contributing

Feel free to extend this project with:
- Additional UI components
- New model integrations
- Advanced features (RAG, additional tools, etc.)
- Production-ready improvements
- Documentation enhancements
- Database migration strategies
- Multi-user authentication
- Custom tool implementations

## 📄 Summary

This project is a beginner-to-intermediate friendly example of a local AI chatbot built with LangGraph and Ollama. It demonstrates how to combine:
- A sophisticated backend graph orchestration (LangGraph)
- A responsive web interface (Streamlit)
- A local large language model (Ollama)
- Persistent data storage (SQLite)
- External tool integration (Search, Calculator, APIs)

to create a powerful, privacy-first conversational AI application without relying on external APIs or cloud services, while also supporting agent capabilities for extended functionality.

---

**Created:** 2026  
**Framework:** LangGraph  
**Language:** Python  
**UI Framework:** Streamlit  
**Model Runtime:** Ollama  
**Database:** SQLite  
**Agent Capabilities:** Tool Calling, Search Integration

Happy coding! 🚀
