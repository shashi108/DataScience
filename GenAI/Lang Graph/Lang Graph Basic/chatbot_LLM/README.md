# AI Chatbot with LangGraph and Ollama

This project demonstrates how to build a simple chatbot using Python, Streamlit, LangGraph, and a local Ollama model. It includes multiple UI variations that show different ways of integrating a LangGraph backend with a chat interface.

## Project purpose

The project is designed to teach and demonstrate:

- how to build a chatbot backend with LangGraph
- how to connect a model using LangChain and Ollama
- how to manage chat state with memory checkpoints
- how to build different Streamlit chat interfaces
- how to stream responses and manage conversation threads

## Tech stack

- Python
- Streamlit
- LangGraph
- LangChain Core
- LangChain Ollama
- Ollama local runtime

## Project structure

```text
chatbot_LLM/
├── backend.py        # LangGraph chatbot graph and model setup
├── ai_app.py         # Styled Streamlit chat app
├── 1app_basic.py     # Basic Streamlit chat app
├── 2app_basic.py     # Chat app with custom CSS styling
├── 3app_stream.py    # Streaming response example
├── 4app_resume.py    # Chat history + thread management example
├── README.md         # Project documentation
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.9+
- pip installed
- Ollama installed and running locally
- a compatible model downloaded, for example:

```bash
ollama pull gemma3:4b
```

Install the required Python packages:

```bash
pip install streamlit langgraph langchain-core langchain-ollama
```

## How it works

### Backend

`backend.py` defines a LangGraph workflow:

- `ChatState` stores conversation messages
- `add_messages` merges chat history
- `chat_node()` sends messages to the LLM
- `MemorySaver` keeps state in memory for the active session
- `ChatOllama(model="gemma3:4b")` loads the local model

### UI examples

The app folder contains several front-end versions:

- `1app_basic.py`: simple chat UI
- `2app_basic.py`: chat UI with custom styling
- `3app_stream.py`: streaming LLM responses in real time
- `4app_resume.py`: chat history and thread management
- `ai_app.py`: more polished chat interface with session state and message styling

## Running the app

From the project directory:

```bash
cd "GenAI/Lang Graph/Lang Graph Basic/chatbot_LLM"
```

### Run the main style app

```bash
streamlit run ai_app.py
```

### Run the basic app

```bash
streamlit run 1app_basic.py
```

### Run the styled basic app

```bash
streamlit run 2app_basic.py
```

### Run the streaming app

```bash
streamlit run 3app_stream.py
```

### Run the resume/thread app

```bash
streamlit run 4app_resume.py
```

## Example workflow

1. Start Ollama locally.
2. Launch a Streamlit app.
3. Enter a prompt in the chat box.
4. The user message is sent to the LangGraph backend.
5. The backend calls the local Ollama model.
6. The answer is returned and displayed in the UI.

## Notes

- This is a learning/demo project rather than a production-ready chatbot.
- Conversation memory is kept in memory only, so it resets when the app restarts.
- You may need to download the chosen model before running the app.
- For real-world usage, you would usually add persistence, user authentication, error handling, logging, and more advanced RAG or tool-calling features.

## Summary

This project is a beginner-friendly example of a local AI chatbot built with LangGraph and Ollama. It shows how to combine a backend graph, a Streamlit interface, and a local LLM to create a basic conversational AI application.
