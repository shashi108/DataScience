# Travel Planning Multi-Agent AI System

A production-ready multi-agent travel planning application built with LangGraph, LangChain, and Streamlit. The system coordinates specialized agents for flights, hotels, weather, budgeting, and itinerary creation to produce a user-ready travel plan.

## Overview

This project allows a user to describe a trip and receive a structured draft itinerary with supporting analysis from multiple AI agents. It combines:

- Flight planning and route guidance
- Hotel and accommodation recommendations
- Weather and forecast analysis
- Budget feasibility checks
- Itinerary generation with human approval
- Streamlit-based web UI for interaction

## Project Structure

```text
Travel Planning Multi-Agent AI System Production-Ready/
├── app.py                    # Streamlit dashboard and user interface
├── app2.py                   # Alternate app implementation
├── agents.py                 # Multi-agent planning logic
├── config.py                 # LLM and environment configuration
├── graph.py                  # LangGraph workflow definition
├── state.py                  # Workflow state schema
├── mcp_client.py             # MCP client for external tools/data sources
├── weather_mcp_server.py     # Weather MCP server
├── requirements.txt          # Python dependencies
├── planner_env_new/          # Environment or workflow assets
├── travel_plans/             # Saved generated travel plans
├── Multi-Agent Travel Planning Workflow.png
├── Supervisor Agent Travel Flowchart.png
├── Supervisor Agent Travel Workflow.png
├── Travel Planning Multi-Agent Architecture.png
└── .env                      # Local environment file (not committed in some setups)
```

## Key Features

- Multi-agent supervisor orchestration using LangGraph
- Specialist agents for:
  - flight_agent
  - hotel_agent
  - weather_agent
  - budget_agent
  - itinerary_agent
- Human-in-the-loop approval step before final plan delivery
- Integrations with:
  - Tavily search
  - AviationStack API
  - OpenWeather API
  - Ollama LLMs or Groq-backed models
  - PostgreSQL checkpointing support

## Tech Stack

- Python
- LangGraph
- LangChain
- Streamlit
- Ollama / Groq LLM backends
- PostgreSQL
- Tavily Search
- AviationStack
- OpenWeather

## Prerequisites

Before running the project, install:

- Python 3.10+
- pip
- PostgreSQL (if using graph checkpointing)
- Ollama (for local model usage), or configure a Groq API key

## Environment Setup

Create a `.env` file in this directory with the required variables, for example:

```bash
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
AVIATIONSTACK_API_KEY=your_aviationstack_key
OPENWEATHER_API_KEY=your_openweather_key
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

Note: The project loads environment variables from `.env` in the same folder using `python-dotenv`.

## Installation

```bash
cd "GenAI/Lang Graph/Travel Planning System/Travel Planning Multi-Agent AI System Production-Ready"
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit UI:

```bash
streamlit run app.py
```

This launches the travel planner interface, where users can:

- enter a trip request
- generate a draft itinerary
- review agent output
- approve or revise the plan
- save the final travel plan as a Markdown file

## Workflow Summary

1. User enters a travel request in the UI.
2. Supervisor agent checks validity and selects relevant specialist agents.
3. Flight, hotel, weather, and budget agents gather information.
4. Itinerary agent composes a draft trip plan.
5. Human approval is requested.
6. Final response agent generates the polished final travel plan.

## Example Request

```text
Plan a 7-day Japan trip under ₹2 lakh. Include flights, hotels, weather, budget, and sightseeing.
```

## Notes

- Some features require external API keys and working services.
- The project uses local LLM configuration via Ollama by default (`ChatOllama(model="qwen3:1.7b")`).
- Generated plans are automatically saved under the `travel_plans/` directory.

## License

This project is provided as-is for educational and experimental use. If you are publishing or distributing it, check whether a project-specific license is required by the original author.

## Author

Shashi Kumar
