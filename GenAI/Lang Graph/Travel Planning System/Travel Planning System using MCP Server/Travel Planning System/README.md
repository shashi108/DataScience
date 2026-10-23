# Travel Planning System using MCP Server

A LangGraph-powered travel planning application that coordinates multiple specialized agents to research flights, hotels, weather, and build a 7-day itinerary for a user request.

This project demonstrates a multi-tool agent workflow using Model Context Protocol (MCP) integrations for external services such as Tavily search and weather data, plus custom MCP server wrappers.

## Overview

The app uses a graph-based workflow to orchestrate several agents:

- Flight agent: gathers candidate airports and airline information
- Hotel agent: searches travel/hotel options
- Weather agent: fetches current conditions and forecasts
- Itinerary agent: synthesizes the results into a day-by-day travel plan

The system stores graph checkpoints in PostgreSQL and is designed to run as a command-line workflow with LangGraph.

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM
- Tavily MCP
- AviationStack MCP
- OpenWeather MCP
- PostgreSQL + PostgresSaver
- Streamlit (present in dependencies for potential UI usage)

## Project Structure

```text
Travel Planning System/
├── app.py
├── custom_weather_mcp_server.py
├── main.py
├── mcp_client.py
├── requirements.txt
├── aviationstack-mcp/
│   └── ...
└── .env
```

## Features

- Multi-agent travel planning workflow
- MCP-based tool integration for external APIs
- Weather and forecast retrieval
- Hotel and travel research via Tavily search
- Flight and airline analysis using AviationStack
- 7-day itinerary generation in Markdown format
- Persistent workflow checkpoints using PostgreSQL

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+
- PostgreSQL server running
- API keys for:
  - Groq
  - Tavily
  - AviationStack
  - OpenWeather

## Environment Variables

Create a `.env` file in this directory with the following values:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
DATABASE_URL=postgresql://username:password@host:port/dbname
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

From this directory:

```bash
python main.py
```

You will be prompted to enter a travel request, for example:

```text
Plan a 7-day trip to Tokyo with a moderate budget.
```

The workflow will run the graph and print the final itinerary.

## Notes

- `main.py` is the primary workflow runner.
- `mcp_client.py` configures the MCP tool servers used by the application.
- `custom_weather_mcp_server.py` exposes weather tools over MCP.
- `app.py` is also present and may be used for additional application entry points or experimentation.
- The project currently contains hardcoded local filesystem paths in `mcp_client.py` for the AviationStack and custom weather MCP executables. These should be adjusted to match your local environment before running the project on a different machine.

## Example Use Case

```text
Enter your travel request: Plan a 7-day trip to Paris for a couple with a hotel near central attractions and a moderate budget.
```

The system will combine travel research and weather insights and produce an itinerary with budget guidance.

## License

This project is provided as-is for educational and research purposes.

## Related Files

- `main.py` — orchestrates the LangGraph travel workflow
- `mcp_client.py` — connects to MCP tools and external APIs
- `custom_weather_mcp_server.py` — custom weather MCP server
- `requirements.txt` — Python dependencies
