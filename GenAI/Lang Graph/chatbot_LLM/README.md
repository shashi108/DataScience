# AI Chatbot with LangGraph and Ollama

This project demonstrates how to build a simple chatbot using Python, Streamlit, LangGraph, and a local Ollama model. It includes multiple UI variations that show different ways of integrating a LangGraph workflow with an interactive Streamlit interface for real-time conversational AI.

## 🎯 Project Purpose

The project is designed to teach and demonstrate:

- How to build a chatbot backend with LangGraph
- How to connect a model using LangChain and Ollama
- How to manage chat state with memory checkpoints
- How to build different Streamlit chat interfaces
- How to stream responses and manage conversation threads
- How to implement stateful conversations with message history
- How to create multiple UI variants for different use cases

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web-based UI framework
- **LangGraph** - Graph-based workflow orchestration
- **LangChain Core** - AI/LLM framework components
- **LangChain Ollama** - Integration with local Ollama models
- **Ollama** - Local LLM runtime (privacy-first, no API calls)

## 📁 Project Structure

```text
chatbot_LLM/
├── backend.py           # LangGraph chatbot graph and model setup
├── ai_app.py            # Main styled Streamlit chat application
├── 1app_basic.py        # Basic Streamlit chat app (minimal UI)
├── 2app_basic.py        # Chat app with custom CSS styling
├── 3app_stream.py       # Streaming response example
├── 4app_resume.py       # Chat history + thread management example
└── README.md            # Project documentation
```

## 📋 Prerequisites

Before running the project, make sure you have:

- **Python 3.9+** - Latest Python version recommended
- **pip** - Python package manager
- **Ollama** - Installed and running locally ([Download here](https://ollama.ai))
- A compatible model downloaded locally (e.g., Gemma, Llama2, Mistral)

### Install Ollama and Download a Model

```bash
# Download and install Ollama from https://ollama.ai
# Then pull a model (example with Gemma 3)
ollama pull gemma3:4b
```

### Install Python Dependencies

```bash
pip install streamlit langgraph langchain-core langchain-ollama
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

### UI Examples

The project includes several front-end implementations:

| App | File | Features | Use Case |
|-----|------|----------|----------|
| **Main App** | `ai_app.py` | Styled interface, session state, message formatting | Production demo |
| **Basic** | `1app_basic.py` | Minimal UI, simple message display | Learning basics |
| **Styled** | `2app_basic.py` | Custom CSS styling, better UX | Development reference |
| **Streaming** | `3app_stream.py` | Real-time response streaming | Advanced streaming patterns |
| **Threaded** | `4app_resume.py` | Chat history, thread management, conversation recovery | Multi-session handling |

## 🏃 Running the App

### Prerequisites Check

Before running, ensure Ollama is running:

```bash
ollama serve
```

(In another terminal, proceed with the commands below)

### Navigate to Project Directory

```bash
cd "GenAI/Lang Graph/Lang Graph Basic/chatbot_LLM"
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

## 📊 Example Workflow

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

## 🔑 Key Features

✅ **Local Processing** - No data sent to external APIs (privacy-first)  
✅ **Stateful Conversations** - Context maintained across messages  
✅ **Multiple UI Patterns** - Examples for different use cases  
✅ **Streaming Support** - Real-time response generation  
✅ **Thread Management** - Handle multiple conversation threads  
✅ **Easy Model Switching** - Change models by updating model name  
✅ **Extensible Architecture** - Easy to add tools, RAG, or other features

## 🔧 Customization Guide

### Change the LLM Model

Edit `backend.py` and modify the model name:

```python
# Current
model = ChatOllama(model="gemma3:4b")

# Change to different model
model = ChatOllama(model="llama2")  # or mistral, neural-chat, etc.
```

### Modify System Prompt

Add custom system instructions to `backend.py`:

```python
system_prompt = """You are a helpful AI assistant specializing in data science and AI topics."""
```

### Add Custom CSS Styling

Modify the Streamlit theme in any app file:

```python
st.set_page_config(page_title="AI Chatbot", layout="wide")
```

## 📝 Notes

- **Demo Project** - This is a learning/demo project rather than production-ready
- **Memory Limitation** - Conversation memory is kept in memory only and resets on app restart
- **Model Download** - Models are downloaded to Ollama cache on first run (may take time)
- **GPU Support** - Ollama can leverage GPU if available for faster inference
- **Production Use** - For real-world deployment, add persistence, authentication, error handling, logging, and advanced RAG/tool-calling features

## 🚀 Production Considerations

For deploying this chatbot to production, consider:

1. **Persistence** - Use database (PostgreSQL, MongoDB) to store conversations
2. **Authentication** - Add user authentication and authorization
3. **Error Handling** - Comprehensive error handling and recovery
4. **Logging** - Implement logging for debugging and monitoring
5. **RAG Integration** - Add Retrieval Augmented Generation for knowledge bases
6. **Tool Calling** - Enable agent capabilities with external tools
7. **Load Testing** - Test under high concurrent user loads
8. **Docker** - Containerize for easy deployment
9. **Environment Variables** - Use .env files for configuration
10. **API Rate Limiting** - Implement rate limiting for stability

## 📚 Learning Path

1. **Start** → Run `1app_basic.py` to understand basic structure
2. **Explore** → Try `2app_basic.py` for styled UI patterns
3. **Advanced** → Run `3app_stream.py` for streaming concepts
4. **Expert** → Use `4app_resume.py` to manage state across sessions
5. **Production** → Customize `ai_app.py` for your use case

## 🤝 Contributing

Feel free to extend this project with:
- Additional UI components
- New model integrations
- Advanced features (RAG, tool-calling, etc.)
- Production-ready improvements
- Documentation enhancements

## 📄 Summary

This project is a beginner-to-intermediate friendly example of a local AI chatbot built with LangGraph and Ollama. It demonstrates how to combine:
- A sophisticated backend graph orchestration (LangGraph)
- A responsive web interface (Streamlit)
- A local large language model (Ollama)

to create a powerful, privacy-first conversational AI application without relying on external APIs or cloud services.

---

**Created:** 2026  
**Framework:** LangGraph  
**Language:** Python  
**UI Framework:** Streamlit  
**Model Runtime:** Ollama

Happy coding! 🚀
