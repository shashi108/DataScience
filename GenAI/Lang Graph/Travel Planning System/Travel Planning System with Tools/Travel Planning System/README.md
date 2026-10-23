# AI Travel Booking System

A multi-agent travel planning application built with LangGraph, Groq, Tavily search, and a Streamlit frontend. The system coordinates specialized agents to gather flight and hotel information, build itineraries, and present a polished final travel plan.

## Overview

This project demonstrates a travel planning workflow where multiple agents collaborate to:

- search for flight options
- look up hotel candidates
- combine findings into a day-wise itinerary
- generate a final travel response for the user

The application supports both:

- a terminal-based CLI workflow via `main.py`
- a browser UI via `app.py` built with Streamlit

## Features

- Multi-agent workflow using LangGraph
- Flight agent powered by AviationStack API
- Hotel research powered by Tavily search
- Itinerary generation using Groq-hosted LLMs
- PostgreSQL checkpointing for state persistence
- Streamlit interface with quick destination suggestions and plan export

## Project structure

```text
Travel Planning System/
├── app.py                  # Streamlit web app
├── main.py                 # LangGraph workflow and CLI runner
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── travel_plans/           # Auto-saved generated travel plans
└── tools/
    ├── flight_tool.py      # AviationStack flight lookup helper
    └── tavily_tool.py      # Tavily search helper
```

## Tech stack

- Python
- LangGraph
- LangChain
- Groq
- Tavily
- AviationStack
- PostgreSQL
- Streamlit

## Environment variables

Create a `.env` file in this directory with the following values:

```env
DATABASE_URL=postgresql://username:password@host:port/dbname
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
```

Notes:

- `DATABASE_URL` is required for the LangGraph Postgres checkpoint saver.
- `GROQ_API_KEY` is required for the LLM-based itinerary and final response generation.
- `TAVILY_API_KEY` is required for hotel and travel research.
- `AVIATIONSTACK_API_KEY` is required for the flight lookup helper.

## Installation

```bash
cd "GenAI/Lang Graph/Travel Planning System/Travel Planning System with Tools/Travel Planning System"
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the application

### CLI mode

```bash
python main.py
```

This starts an interactive prompt where you can enter a travel request.

### Streamlit app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal and describe your trip.

## Agent workflow

The workflow is built around four main stages:

1. `flight_agent`  
   Searches for flight-related information.

2. `hotel_agent`  
   Uses Tavily to find hotel and travel-related recommendations.

3. `itinerary_agent`  
   Creates a travel itinerary from the combined flight and hotel context.

4. `final_agent`  
   Produces the final user-facing travel plan.

## Example usage

```text
Enter your travel request: Plan a 5-day trip to Mumbai with flights and hotels under ₹50,000
```

The system will generate a final travel plan with:

- trip summary
- flight information
- hotel suggestions
- day-wise itinerary
- important considerations

## Important notes

- The application is designed to provide research-backed recommendations, not guaranteed bookings.
- Flight and hotel availability may be limited by API access and live data constraints.
- Any generated itinerary should be reviewed before purchase or booking.

## License

This project is intended for personal learning and experimentation. Add your preferred license if you are publishing it publicly.

## Acknowledgements

This project uses:

- LangGraph for orchestrating the agent workflow
- LangChain and Groq for LLM interaction
- Tavily for web search
- AviationStack for flight data
- Streamlit for the interactive interface
