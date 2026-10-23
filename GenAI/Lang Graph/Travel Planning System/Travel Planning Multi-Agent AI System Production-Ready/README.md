# Travel Planning Multi-Agent AI System

A production-ready multi-agent travel planning application built with Python, LangGraph, LangChain, and Streamlit. The system coordinates specialized agents for flights, hotels, weather, budgeting, and itinerary generation to help users create structured trip plans from a single natural-language request.

## Overview

This project allows a user to describe a trip in plain English and receive a structured draft itinerary with supporting reasoning from multiple AI agents. It follows a human-in-the-loop workflow:

1. A supervisor validates the request.
2. Relevant specialist agents are selected.
3. Agents gather and analyze travel information.
4. A draft itinerary is generated.
5. Human approval is requested.
6. A final polished trip plan is created.

The application is designed for experimentation, prototyping, and local deployment using open-source or cloud-based LLM backends.

## Key Features

- Multi-agent orchestration with LangGraph
- Specialist travel agents for:
  - flight planning
  - hotel and stay recommendations
  - weather analysis
  - budget assessment
  - final itinerary generation
- Human approval step before final plan delivery
- Integration with Tavily search, aviation APIs, and weather APIs
- Streamlit-based interactive user interface
- Supports local and cloud LLM providers
- Saves generated travel plans in the `travel_plans/` directory

## Architecture

The system is structured around a LangGraph workflow where a supervisor routes work to specialist agents. Each agent works on its domain and contributes results to a shared state object that is used later by the itinerary and final response stages.

Core workflow components:

- `app.py` — main Streamlit UI
- `app2.py` — alternate app implementation
- `agents.py` — agent definitions and orchestration logic
- `graph.py` — workflow graph construction
- `state.py` — graph state schema
- `config.py` — environment configuration and LLM setup
- `mcp_client.py` — MCP integrations for external tools and data sources
- `weather_mcp_server.py` — weather tool server

## Project Structure

```text
Travel Planning Multi-Agent AI System Production-Ready/
├── app.py                          # Main Streamlit application
├── app2.py                         # Alternative app entry point
├── agents.py                       # Agent logic and workflow behavior
├── config.py                      # LLM and environment configuration
├── graph.py                       # LangGraph graph definition
├── state.py                       # Travel workflow state schema
├── mcp_client.py                  # MCP client and API integrations
├── weather_mcp_server.py          # Weather MCP server
├── requirements.txt               # Python dependencies
├── planner_env_new/               # Additional workflow/environment assets
├── travel_plans/                  # Generated travel plans
├── Multi-Agent Travel Planning Workflow.png
├── Supervisor Agent Travel Flowchart.png
├── Supervisor Agent Travel Workflow.png
├── Travel Planning Multi-Agent Architecture.png
├── README.md
├── .env                          # Local environment file (not always committed)
├── .venv                         # Optional local virtual environment
└── .gitignore                    # Git ignore configuration (if present)
```

## Tech Stack

- Python 3.10+
- LangGraph
- LangChain
- LangChain Community
- Streamlit
- Ollama / Groq for LLM inference
- Tavily Search
- Aviation Stack API
- OpenWeather API
- PostgreSQL (optional checkpoint support)

## Prerequisites

Before running the project, ensure you have:

- Python 3.10 or newer
- `pip` installed
- `git` installed
- Optional: PostgreSQL if using checkpointing or database-backed state
- Optional: Ollama installed locally for local model inference

## Environment Setup

Create a `.env` file in this directory with the required variables:

```bash
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
AVIATIONSTACK_API_KEY=your_aviationstack_key
OPENWEATHER_API_KEY=your_openweather_key
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

The project loads environment variables from the same folder using `python-dotenv`.

If you are using Ollama locally, install and pull the model:

```bash
ollama pull qwen3:1.7b
```

## Installation

From the repository root:

```bash
cd "GenAI/Lang Graph/Travel Planning System/Travel Planning Multi-Agent AI System Production-Ready"
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Application

Start the main Streamlit app:

```bash
streamlit run app.py
```

This launches the travel planner interface where users can:

- enter a trip request
- generate a draft itinerary
- review specialist agent findings
- approve or revise the plan
- save the final output as a Markdown travel plan

## Example Use

```text
Plan a 7-day trip to Japan under ₹2 lakh. Include flights, hotel suggestions, weather, budget analysis, and a sightseeing itinerary.
```

## Workflow Summary

1. User enters a travel request.
2. Supervisor validates the request and selects relevant agents.
3. Flight, hotel, weather, and budget agents gather information.
4. Itinerary agent creates a draft travel plan.
5. Human approval is requested.
6. Final response agent generates the final polished plan.

## Notes

- Some features depend on external APIs and valid keys.
- The default configuration in `config.py` uses Ollama with `qwen3:1.7b`.
- You can switch to Groq by uncommenting the Groq configuration block.
- Generated plans are saved under the `travel_plans/` directory.
- This project is primarily intended for learning, prototyping, and experimentation.

## License

This project is provided as-is for learning and experimentation. If you plan to publish, redistribute, or commercialize it, check whether a project-specific license or attribution requirement applies.

## Author

Shashi Kumar
