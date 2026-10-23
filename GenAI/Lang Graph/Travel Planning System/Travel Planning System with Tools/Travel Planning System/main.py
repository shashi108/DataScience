import os
import operator
from typing import Annotated, TypedDict

import psycopg
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights


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

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0,
)
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

    # Each executed agent contributes 1 to this counter.
    agent_runs: Annotated[int, operator.add]

# --------------------------------------------------
# 4. Flight Agent
# --------------------------------------------------

def flight_agent(state: TravelState) -> dict:
    """Search for flight-related information."""
    print("✈️ Flight Agent started")
    try:
        flight_data = search_flights(state["user_query"])
    except Exception as exc:
        flight_data = f"Flight search error: {exc}"
    print("✈️ Flight Agent completed")
    return {
        "flight_results": flight_data,
        "messages": [AIMessage(content="Flight search completed.")],
        "agent_runs": 1,
    }

# --------------------------------------------------
# 5. Hotel Agent
# --------------------------------------------------
def hotel_agent(state: TravelState) -> dict:
    """Search for hotels related to the travel request."""
    print("🏨 Hotel Agent started")
    query = (
        "Find suitable hotels for this travel request. "
        "Identify the destination, dates, budget, and preferences "
        "if available. Do not invent prices or availability.\n\n"
        f"Travel request: {state['user_query']}"
    )
    try:
        hotel_data = tavily_search(query)
    except Exception as exc:
        hotel_data = f"Hotel search error: {exc}"
    print("🏨 Hotel Agent completed")
    return {
        "hotel_results": hotel_data,
        "messages": [AIMessage(content="Hotel search completed.")],
        "agent_runs": 1,
    }
# --------------------------------------------------
# 6. Itinerary Agent
# --------------------------------------------------
def itinerary_agent(state: TravelState) -> dict:
    """Create an itinerary from the available search information."""
    print("🗓️ Itinerary Agent started")
    prompt = f"""
Create a practical travel itinerary using the information below.
USER REQUEST:{state['user_query']}
FLIGHT SEARCH RESULTS:{state['flight_results']}
HOTEL SEARCH RESULTS:{state['hotel_results']}

Instructions:
1. Organize the itinerary by day.
2. Consider the user's destination and trip duration.
3. Use the available flight and hotel information.
4. Do not invent flight schedules, fares, hotel prices, or availability.
5. Clearly identify information that has not been verified.
6. If dates, duration, or budget are missing, mention the assumptions.
7. Suggest sightseeing only when appropriate for the destination.
"""

    try:
        response = llm.invoke([
            SystemMessage(
                content=(
                    "You are a careful travel itinerary planner. "
                    "Distinguish verified search information from "
                    "suggestions and assumptions."
                )
            ),
            HumanMessage(content=prompt),
        ])

        itinerary = str(response.content)

    except Exception as exc:
        itinerary = (
            "Itinerary generation failed. "
            f"Please retry. Error: {exc}"
        )
    print("🗓️ Itinerary Agent completed")
    return {
        "itinerary": itinerary,
        "messages": [AIMessage(content=itinerary)],
        "agent_runs": 1,
    }


# --------------------------------------------------
# 7. Final Response Agent
# --------------------------------------------------

def final_agent(state: TravelState) -> dict:
    """Combine the search results and itinerary into a final answer."""

    print("📝 Final Response Agent started")

    prompt = f"""
Prepare the final response for the user's travel request.

USER REQUEST:{state['user_query']}
FLIGHT INFORMATION:{state['flight_results']}
HOTEL INFORMATION:{state['hotel_results']}
PROPOSED ITINERARY:{state['itinerary']}

Response format:
1. Trip summary
2. Flight information
3. Hotel recommendations
4. Day-wise itinerary
5. Important considerations

Rules:
- Never claim that a ticket or hotel has been booked.
- Never invent prices, flight numbers, schedules, or availability.
- Clearly label demo data and unverified web search information.
- State when information is missing.
- Provide a clear, readable response.
"""

    try:
        response = llm.invoke([
            SystemMessage(
                content=(
                    "You are a helpful travel planning assistant. "
                    "Be accurate and transparent about uncertainty."
                )
            ),
            HumanMessage(content=prompt),
        ])

        final_response = str(response.content)

    except Exception as exc:
        # Keep the application useful if final formatting fails.
        final_response = (
            "Final response generation failed.\n\n"
            f"Available itinerary:\n{state['itinerary']}\n\n"
            f"Error: {exc}"
        )

    print("📝 Final Response Agent completed")

    return {
        "final_response": final_response,
        "messages": [
            AIMessage(content=final_response)
        ],
        "agent_runs": 1,
    }


# --------------------------------------------------
# 8. Build the graph
# --------------------------------------------------

def build_graph(checkpointer=None):
    """Create the travel workflow."""

    graph = StateGraph(TravelState)

    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("final_agent", final_agent)

    # Start flight and hotel searches independently.
    graph.add_edge(START, "flight_agent")
    graph.add_edge(START, "hotel_agent")

    # Wait until BOTH searches have completed.
    graph.add_edge(
        ["flight_agent", "hotel_agent"],
        "itinerary_agent",
    )

    graph.add_edge("itinerary_agent", "final_agent")
    graph.add_edge("final_agent", END)

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

    user_input = input(
        "\nEnter your travel request: "
    ).strip()

    if not user_input:
        print("Please enter a travel request.")
        return

    # Use a stable thread ID for this CLI conversation.
    # Change it to start a separate conversation.
    thread_id = input(
        "Enter thread ID [travel_user_1]: "
    ).strip() or "travel_user_1"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state: TravelState = {
        "messages": [
            HumanMessage(content=user_input)
        ],
        "user_query": user_input,
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "agent_runs": 0,
    }

    try:
        result = app.invoke(
            initial_state,
            config=config,
        )

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