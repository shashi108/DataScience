# AI Chatbot with LangGraph and Ollama

This project is a simple conversational chatbot built with Python, Streamlit, LangGraph, and a local Ollama LLM. It demonstrates how to create a stateful chatbot graph that accepts user messages, sends them to an LLM, and returns a response while preserving chat state in memory.

## Project purpose

The application is designed to:

- accept user input from a Streamlit web interface
- pass the conversation into a LangGraph workflow
- call a local LLM hosted with Ollama
- maintain conversation state using LangGraph memory checkpointing
- show the response back in a chat UI

This is a beginner-friendly example for learning:

- LangGraph fundamentals
- stateful agent/chat workflows
- local LLM integration using Ollama
- Streamlit chatbot UI development

## Tech stack

- Python
- Streamlit
- LangGraph
- LangChain Core
- LangChain Ollama
- Ollama local model runtime

## Project structure

```text
chatbot_LLM/
├── ai_app.py          # Streamlit chat interface with custom styling
├── app_basic.py       # Basic chatbot example
├── app_basic2.py      # Alternate Streamlit chatbot app
├── backend.py         # LangGraph chatbot backend and model setup
├── README.md          # Project documentation
```

## How it works

### 1. Backend graph
In `backend.py`:

- a `ChatState` is defined using `TypedDict`
- messages are managed through `add_messages`
- a `chat_node()` function sends the conversation to the LLM
- the workflow is built using `StateGraph`
- `MemorySaver` is used to keep chat state in memory
- the model is initialized with `ChatOllama(model="gemma3:4b")`

This means each message is treated as part of the graph state and the LLM response is appended back to the message list.

### 2. UI layer
The Streamlit apps (`ai_app.py` and `app_basic2.py`) provide a simple chat interface where users can type messages and see responses.

The UI:

- displays the chat history
- sends the latest user message to the backend
- receives the model response
- renders both user and assistant messages in the interface

### 3. Local model execution
The project uses Ollama to run a local model instead of requiring a cloud-based LLM API. This is useful for:

- local experimentation
- offline development
- lower-cost testing
- learning LLM application workflows without external API keys

## Requirements

Before running the project, make sure you have:

- Python 3.9+
- pip installed
- Ollama installed and running locally
- a compatible model downloaded, such as:

```bash
ollama pull gemma3:4b
```

You should also install the required Python packages:

```bash
pip install streamlit langgraph langchain-core langchain-ollama
```

## Running the app

### Option 1: Use the main Streamlit app

```bash
cd "GenAI/Lang Graph/Lang Graph Basic/chatbot_LLM"
streamlit run ai_app.py
```

### Option 2: Run alternative app

```bash
cd "GenAI/Lang Graph/Lang Graph Basic/chatbot_LLM"
streamlit run app_basic2.py
```

## Example flow

1. Start Ollama
2. Launch the Streamlit application
3. Enter a prompt in the chat box
4. The backend sends the message to the LangGraph workflow
5. The LLM responds using the local model
6. The response appears in the chat window

## Notes

- This project is a learning/demo project rather than a production-ready chatbot.
- It uses in-memory checkpoints, so state is lost when the app restarts.
- The model is configured to use `gemma3:4b`, which may need to be downloaded locally first.
- For more advanced chatbots, you would typically add features such as:
  - conversation memory beyond a single session
  - retrieval-augmented generation (RAG)
  - tool calling
  - better error handling
  - external database storage

## Learning goals

This project is useful for understanding:

- how chatbots are structured in LangGraph
- how to connect models with custom graph state
- how Streamlit can be used for interactive AI interfaces
- how local LLMs can be used without cloud API dependencies

## Summary

This project is a compact, beginner-friendly example of a local AI chatbot using LangGraph and Ollama. It combines a backend graph, a Streamlit front-end, and a local LLM to demonstrate how modern conversational AI applications are structured.


