# Travel Planning Multi-Agent AI System

A full-stack AI travel assistant built with Python, LangGraph, LangChain, and Streamlit. The project uses multiple specialized agents to plan trips, evaluate travel constraints, and generate a human-reviewed itinerary before producing a final travel plan.

This application is designed for local experimentation and prototyping, while also supporting realistic travel workflows such as flight lookup, hotel suggestions, weather analysis, budget review, and itinerary generation.

## Overview

The system accepts a natural-language trip request such as:

```text
Plan a 7-day trip to Japan under ₹2 lakh. Include flights, hotel suggestions, weather, budget analysis, and a sightseeing itinerary.
```

It then:

1. Validates the user request with a supervisor guardrail.
2. Selects the relevant specialist agents.
3. Gathers flight, hotel, weather, and budget data.
4. Generates a draft itinerary.
5. Requests human approval.
6. Produces a polished final travel plan.

## Key Features

- Multi-agent orchestration using LangGraph
- Real travel workflow with specialized agents:
  - Flight planning
  - Hotel recommendations
  - Weather analysis
  - Budget assessment
  - Itinerary construction
  - Final response synthesis
- Human-in-the-loop approval step before final output
- Streamlit web interface for interactive trip planning
- Integration with external tools such as:
  - Tavily Search
  - AviationStack APIs
  - OpenWeatherMap APIs
  - Optional PostgreSQL checkpointing
- Local model support via Ollama and cloud options via Groq
- Saves generated travel plans to the `travel_plans/` directory

## Architecture

The app follows a supervisor-driven agent workflow:

```text
User Request
    ↓
Supervisor Agent
    ├── Flight Agent
    ├── Hotel Agent
    ├── Weather Agent
    ├── Budget Agent
    └── Itinerary Agent
    ↓
Human Approval
    ↓
Final Response Agent
```

The workflow is defined in `graph.py` and coordinated through `state.py`, while the actual agent logic lives in `agents.py`.

## Repository Structure

```text
Travel Planning Multi-Agent AI System Production-Ready/
├── app.py                       # Main Streamlit user interface
├── app2.py                      # Alternative app entry point
├── agents.py                    # Agent logic and orchestration
├── config.py                    # LLM and environment configuration
├── graph.py                     # LangGraph workflow graph
├── state.py                     # Shared workflow state schema
├── mcp_client.py                # MCP client and external integrations
├── weather_mcp_server.py        # Weather MCP server
├── requirements.txt             # Python dependencies
├── planner_env_new/             # Supporting environment assets
├── travel_plans/                # Auto-saved generated plan files
├── Multi-Agent Travel Planning Workflow.png
├── Supervisor Agent Travel Flowchart.png
├── Supervisor Agent Travel Workflow.png
├── Travel Planning Multi-Agent Architecture.png
├── README.md
├── .env                        # Local environment variables (not always committed)
├── .venv                       # Optional local virtual environment
├── .gitignore                  # Git ignore settings
└── LICENSE                     # If present in your environment
```

## Tech Stack

- Python 3.10+
- LangGraph
- LangChain
- LangChain Community
- LangChain Ollama
- Streamlit
- Tavily Search
- AviationStack
- OpenWeather API
- PostgreSQL (optional checkpointing)
- Groq and Ollama for LLM backends

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- `pip` installed
- `git` installed
- An API key for at least one supported LLM/provider path
- Optional: PostgreSQL for checkpoint persistence
- Optional: Ollama installed for local LLM inference

## Environment Setup

Create a `.env` file in the project directory and add the required values:

```bash
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
AVIATIONSTACK_API_KEY=your_aviationstack_key
OPENWEATHER_API_KEY=your_openweather_key
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

The project loads environment variables using `python-dotenv`.

If you are using Ollama locally, pull a model before running:

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

## Optional PostgreSQL Setup

If you want to enable PostgreSQL-backed checkpointing, install PostgreSQL and create a database:

```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu / Debian
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE DATABASE travel_planner;"
sudo -u postgres psql -d travel_planner -c "CREATE USER travel_user WITH ENCRYPTED PASSWORD 'your_password';"
sudo -u postgres psql -d travel_planner -c "GRANT ALL PRIVILEGES ON DATABASE travel_planner TO travel_user;"
```

Then add the database URL to your `.env`:

```bash
DATABASE_URL=postgresql://travel_user:your_password@localhost:5432/travel_planner
```

If you are not using PostgreSQL checkpointing, you can leave `DATABASE_URL` empty or unset.

## Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

This launches the travel planner UI where you can:

- Enter a trip request
- Generate a draft itinerary
- Review flight, hotel, weather, and budget insights
- Approve or revise the plan
- Save the final output as a Markdown travel plan

## Example Prompts

```text
Plan a 7-day trip to Japan under ₹2 lakh. Include flights, hotels, weather, budget analysis, and a sightseeing itinerary.
```

```text
Create a 5-day travel plan to Mumbai under ₹40,000 with hotel suggestions and a balanced budget.
```

## Workflow Summary

1. User submits a travel request.
2. Supervisor validates the request and selects the relevant agents.
3. Flight, hotel, weather, and budget agents gather data.
4. Itinerary agent creates a draft route plan.
5. Human approval is requested.
6. Final response agent produces the polished final travel plan.

## Generated Output

After final approval, the app saves the completed itinerary as a Markdown file inside:

```text
travel_plans/
```

Each file includes the generated travel plan and metadata such as timestamp, user ID, and thread ID.

## Notes

- Some features rely on valid external API keys.
- The default configuration in `config.py` uses Ollama with `qwen3:1.7b`.
- You can switch to Groq by uncommenting the Groq configuration block.
- This project is primarily intended for learning, prototyping, and experimentation.
- For production deployment, you may need additional security, monitoring, and operational hardening.

## License

This project is provided as-is for learning and experimentation. If you plan to publish, redistribute, or commercialize it, confirm whether any project-specific licensing or attribution requirements apply.

## Author

Shashi Kumar

## Screenshots

The project includes workflow and architecture diagrams in the same directory:

- `Multi-Agent Travel Planning Workflow.png`
- `Supervisor Agent Travel Flowchart.png`
- `Supervisor Agent Travel Workflow.png`
- `Travel Planning Multi-Agent Architecture.png`

These assets help visualize the agent interaction flow and system design.

## Troubleshooting

If the app does not start correctly:

- Confirm that all required environment variables are set in `.env`.
- Ensure the correct Python virtual environment is active.
- Install dependencies with `pip install -r requirements.txt`.
- Check that the selected LLM backend is available locally or that your API keys are valid.
- If PostgreSQL is enabled, verify that `DATABASE_URL` is correct and the database is reachable.

If you want, I can also help you improve the project further by adding:

- a proper `requirements-dev.txt`
- a `Dockerfile` and `docker-compose.yml`
- a better `LICENSE` section
- a clean project screenshot gallery in the README
- a more professional architecture diagram section
