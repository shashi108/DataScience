import os
import operator
from typing import Annotated, TypedDict
import asyncio
import psycopg
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
import uuid
from langchain_core.messages import (AnyMessage,HumanMessage,AIMessage,SystemMessage)
from langchain_groq import ChatGroq
from mcp_client import (
    tavily_mcp_search,
    aviation_mcp_call,
    extract_destination,
    forecast_mcp_search,weather_mcp_search
)

# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

# --------------------------------------------------
# 2. Initialize the language model
# --------------------------------------------------
llm = ChatGroq(model="openai/gpt-oss-120b",api_key=GROQ_API_KEY, temperature=0)
# --------------------------------------------------
# 3. Define the shared graph state
# --------------------------------------------------

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    final_response: str
    weather_results: str

    # Each executed agent contributes 1 to this counter.
    agent_runs: Annotated[int, operator.add]

# --------------------------------------------------
# 4. Flight Agent
# --------------------------------------------------

# Flight Tool Router Prompt
FLIGHT_AGENT_PROMPT = """
You are a travel flight expert.

User Query:{query}
Airport Information:{airport_data}
Airline Information:{airline_data}

Generate:

1. Likely departure airport
2. Likely arrival airport
3. Airlines serving this route
4. Typical flight duration
5. Estimated airfare range
6. Peak season pricing warning
7. Booking advice

Return concise travel guidance.
"""
# Flight Agent
def flight_agent(state: TravelState):
    print("\nINSIDE FLIGHT AGENT\n")
    query = state["user_query"]

    try:
        airports = asyncio.run(aviation_mcp_call("list_airports"))
        airlines = asyncio.run(aviation_mcp_call( "list_airlines"))

        prompt = FLIGHT_AGENT_PROMPT.format(
            query=query,
            airport_data=str(airports)[:3000],
            airline_data=str(airlines)[:3000]
        )

        response = llm.invoke([
            SystemMessage(content="You are an expert travel flight planner."),
            HumanMessage(content=prompt)
        ])

        flight_data = response.content

    except Exception as e:
        flight_data = f"Flight information unavailable: {str(e)}"
    return {
        "flight_results": flight_data,
        "messages": [AIMessage(content="Flight recommendations generated")],
        "agent_runs": 1
    }

# --------------------------------------------------
# 5. Hotel Agent
# --------------------------------------------------

def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = asyncio.run(tavily_mcp_search(query))
    return {
        "hotel_results": hotel_results,
        "messages": [AIMessage(content="Hotel information fetched")],
       "agent_runs": 1
    }

# --------------------------------------------------
# 5. Weather Agent                                    
# --------------------------------------------------
def weather_agent(state: TravelState):
    city = extract_destination(state["user_query"])
    weather_data = asyncio.run(weather_mcp_search(city))
    forecast_data = asyncio.run(forecast_mcp_search(city))
    return {
        "weather_results": f"""
        Current Weather:{weather_data}
        Forecast:{forecast_data}
        """,
        "messages": [AIMessage(content="Weather information fetched")],
        "agent_runs": 1
    }

# --------------------------------------------------
# 6. Itinerary Agent
# --------------------------------------------------

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a practical 7-day travel itinerary using the information provided by the travel agents.
    User Query:{state['user_query']}
    Flight Results:{state['flight_results']}
    Hotel Results:{state['hotel_results']}
    Weather Information:{state['weather_results']}

    ACCURACY RULES:
1. Never claim that a price is verified unless the tool output
   explicitly provides that price.
2. Never invent flight fares, flight availability, hotel rates,
   room availability, or booking confirmations.
3. AviationStack airport, airline, and schedule data must not be
   presented as live ticket pricing.
4. Use weather data only for the city and dates supported by
   the tool response. Do not invent a seven-day forecast.
5. If information is missing, write "Not verified" or provide
   a clearly labelled estimate with its assumptions.
6. Include realistic travel times, meal breaks, and sightseeing
   hours. Avoid an unnecessarily rushed itinerary.
7. Make sure the itinerary covers exactly seven calendar days.
8. Separate verified tool results, estimates, and recommendations.
9. Calculate the budget consistently. Clearly state the number
    of travellers, hotel rooms, and whether transport is shared.
10. Do not describe a source as verified unless the returned
    tool data supports the claim.
11. End with a summary of missing information needed to improve
    the itinerary.

Return the final answer in readable Markdown with:
- Day-by-day itinerary
- Flight information
- Hotel options
- Ground transportation
- Food and activity budget
- Estimated total budget
- Weather and packing advice
- Assumptions and unverified informatio
    """
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner"),
        HumanMessage(content=prompt)])
    return {
        "itinerary": response.content,
        "final_response": response.content,
        "messages": [response],
        "agent_runs": 1
    }
# --------------------------------------------------
# 8. Build the graph
# --------------------------------------------------

def build_graph(checkpointer=None):
    """Create the travel workflow."""

    graph = StateGraph(TravelState)

    #----- Node -------------
    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("weather_agent", weather_agent)
    graph.add_node("itinerary_agent", itinerary_agent)

    #---- Edge ------------
    graph.add_edge(START, "flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "weather_agent")
    graph.add_edge("weather_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", END)

    return graph.compile(checkpointer=checkpointer)


# --------------------------------------------------
# 9. Initialize PostgreSQL checkpointing
# --------------------------------------------------

# autocommit and prepare_threshold=0 follow the
# recommended connection configuration for PostgresSaver.

_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
    prepare_threshold=0,
)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = build_graph(checkpointer=checkpointer)
# --------------------------------------------------
# 10. Run the application from the terminal
# --------------------------------------------------

def run_cli():
    """Run one travel request from the command line."""

    user_input = input("Enter your travel request: ").strip()

    if not user_input:
        print("Please enter a travel request.")
        return

    # Use a stable thread ID for this CLI conversation.
    # Change it to start a separate conversation.
    thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}

    initial_state: TravelState = {
    "messages": [HumanMessage(content=user_input)],
    "user_query": user_input,
    "flight_results": "",
    "hotel_results": "",
    "weather_results": "",
    "itinerary": "",
    "final_response": "",
    "agent_runs": 0,
    }
    try:
        result = app.invoke(initial_state,config=config,)
        print("\n" + "=" * 60)
        print("FINAL TRAVEL PLAN")
        print("=" * 60)
        print(result["final_response"])

        print(
            f"\nAgent executions in this invocation: "
            f"{result['agent_runs']}"
        )

    except Exception as exc:
        print(f"\nWorkflow failed: {exc}")


if __name__ == "__main__":
    try:
        run_cli()
    finally:
        _conn.close()