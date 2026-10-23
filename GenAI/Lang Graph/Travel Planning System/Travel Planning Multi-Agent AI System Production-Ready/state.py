from typing import Annotated, Any, TypedDict
import operator
from langchain_core.messages import AnyMessage

# --------------------------------------------------
# Define the shared graph state                  
# --------------------------------------------------

class TravelState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], operator.add]
    user_id: str
    user_query: str

    trip_constraints: dict[str, Any]
    selected_agents: list[str] # list of required agents
    supervisor_reasoning: str  #Explain the reason behind the agent selection

    flight_results: str
    hotel_results: str
    weather_results: str
    budget_results: str
    itinerary: str

    approval_request: str
    human_feedback: str
    approved: bool

    final_response: str
    llm_calls: int
