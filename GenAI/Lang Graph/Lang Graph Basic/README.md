# Lang Graph Basic

This folder contains a practical set of notebooks covering the fundamentals of LangGraph, LangChain, prompt orchestration, conditional workflows, and agentic AI patterns.

The examples move from simple LLM interactions to more advanced workflows such as:

- prompt chaining
- parallelized execution
- conditional routing
- iterative generation
- chatbot design
- tool use integration
- MCP-based workflows

## Project Focus

This learning path is designed to help understand how to build LLM-powered applications using structured, stateful workflows instead of isolated prompt calls.

Core topics covered:

- LangChain basics
- Prompt engineering
- LLM-driven decision making
- Multi-step workflows
- Chatbot persistence and UI integration
- Tool calling and workflow automation
- Model Context Protocol (MCP)
- Agentic orchestration with LangGraph

## Notebook Overview

### Foundations and workflows

- `01_BMI_Calculator.ipynb` — simple calculator-style workflow using LLM-driven logic
- `02_BMI_Calculator_Category.ipynb` — classification based on BMI calculation
- `03_LLM_QA.ipynb` — basic question answering using an LLM
- `04_Prompt Chaining.ipynb` — chained prompts for sequential reasoning
- `05_Cricket_Parallel_workflow.ipynb` — parallel workflow execution for multiple tasks
- `06_Evaluate_Essay_parallelization_workflow.ipynb` — parallel evaluation workflow for generated content

### Conditional and iterative logic

- `07_Quadratic Equation Conditional Workflow (Without LLM).ipynb` — conditional logic without an LLM
- `08_LLM Based Review handling conditional workflow.ipynb` — LLM-based review and decision branching
- `09_Iterative work flow_generate tweet.ipynb` — iterative generation workflow

### Chatbots and interaction patterns

- `10_Chatbot_without Persistance.ipynb` — basic chatbot without memory
- `11_Chatbot_with Persistance.ipynb` — stateful chatbot with persistence
- `12_Chatbot_Case Study_With_UI.ipynb` — chatbot case study with user interface
- `Basic Chatbot.ipynb` — general end-to-end chatbot example

### Tools and advanced AI systems

- `13_Tools in Lang Chain_Lang Graph.ipynb` — tool calling in LangChain/LangGraph
- `14_MCP.ipynb` — Model Context Protocol examples
- `15_MCP_Langgraph.ipynb` — MCP integrated with LangGraph
- `Demo client` — demo application client
- `MCP Demo` — MCP demonstration project
- `MCP Demo Remote` — remote MCP demo setup

## Requirements

To run the notebooks successfully, install the following:

```bash
pip install python-dotenv langchain langgraph openai jupyter ipykernel
```

Depending on the notebook, additional libraries may be required such as:

- pandas
- numpy
- requests
- streamlit
- fastapi
- pydantic

## Suggested Workflow

1. Start from the basic notebooks (`01` to `04`)
2. Move to conditional and iterative workflows (`05` to `09`)
3. Explore chatbot implementation patterns (`10` to `12`)
4. Learn tool integration and MCP concepts (`13` to `15`)

## Recommended Setup

- Python 3.9+
- Jupyter Notebook or VS Code with Python extension
- API key configured for the selected LLM provider
- Virtual environment for dependency isolation

## Example Environment Variables

```bash
OPENAI_API_KEY=your_key_here
```

You may also use other providers supported by LangChain or LangGraph depending on the notebook implementation.

## Notes

This folder is intended for hands-on learning and experimentation. It is best used a notebook-by-notebook progression from beginner to advanced agentic workflow patterns.

## Repository Context

This directory belongs to the repository:

- `shashi108/DataScience`

It is part of the broader Generative AI learning path and demonstrates foundational to intermediate LangGraph and LLM orchestration concepts.

---

Built for learning, experimentation, and practical AI workflow development.
