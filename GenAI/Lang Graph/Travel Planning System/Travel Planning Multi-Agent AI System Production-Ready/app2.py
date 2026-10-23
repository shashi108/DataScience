
import uuid

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from graph import app


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Real-World Multi-Agent Travel Planner",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ Real-World Multi-Agent Travel Planner")

st.caption(
    "Plan your trip using AI agents for flights, hotels, "
    "weather, budgeting, and itinerary generation."
)


# ==================================================
# 2. INITIALIZE SESSION STATE
# ==================================================
if "thread_id" not in st.session_state:
    st.session_state.thread_id = (
        f"demo_user_{uuid.uuid4().hex[:8]}"
    )

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False

if "active_query" not in st.session_state:
    st.session_state.active_query = ""


# ==================================================
# 3. SIDEBAR: USER AND THREAD MANAGEMENT
# ==================================================
with st.sidebar:
    st.header("⚙️ Session Settings")

    user_id = st.text_input(
        "User ID",
        value="demo_user",
        key="user_id_input",
    ).strip()

    if not user_id:
        user_id = "demo_user"

    if st.button("🆕 New Thread", use_container_width=True):
        st.session_state.thread_id = (
            f"{user_id}_{uuid.uuid4().hex[:8]}"
        )

        st.session_state.latest_result = None
        st.session_state.waiting_for_approval = False
        st.session_state.active_query = ""

        st.rerun()

    st.divider()

    st.subheader("Current Session")

    st.caption(f"User ID: {user_id}")
    st.code(st.session_state.thread_id)

    st.info(
        "Each thread has a unique ID. If your LangGraph "
        "application uses a checkpointer, its state can "
        "be persisted against this thread."
    )


# ==================================================
# 4. LANGGRAPH CONFIGURATION
# ==================================================
config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}


# ==================================================
# 5. TRAVEL REQUEST INPUT
# ==================================================
st.header("🌍 Plan Your Trip")

query = st.text_area(
    "Enter your travel requirements",
    value=st.session_state.active_query,
    placeholder=(
        "Plan a 7-day Japan trip under Rs. 2 lakh. "
        "I prefer budget hotels and no overnight flights."
    ),
    height=120,
    key="travel_request",
)

create_plan = st.button(
    "🚀 Create Draft Plan",
    type="primary",
    use_container_width=True,
)


# ==================================================
# 6. INVOKE LANGGRAPH TO GENERATE DRAFT
# ==================================================
if create_plan:

    if not query.strip():
        st.warning("Please enter your travel requirements.")

    else:
        st.session_state.active_query = query.strip()

        # Reset old results before starting a new plan
        st.session_state.latest_result = None
        st.session_state.waiting_for_approval = False

        initial_state = {
            "messages": [
                HumanMessage(content=query.strip())
            ],
            "user_id": user_id,
            "user_query": query.strip(),
            "flight_results": "",
            "hotel_results": "",
            "weather_results": "",
            "budget_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }

        try:
            with st.spinner(
                "AI agents are researching and preparing your trip..."
            ):
                result = app.invoke(
                    initial_state,
                    config=config,
                )

            st.session_state.latest_result = result

            st.session_state.waiting_for_approval = (
                "__interrupt__" in result
            )

            st.rerun()

        except Exception as exc:
            st.error("Unable to generate the draft travel plan.")
            st.exception(exc)


# ==================================================
# 7. DISPLAY AGENT RESULTS
# ==================================================
result = st.session_state.latest_result


if result:

    st.divider()
    st.header("📋 Travel Planning Results")

    # ----------------------------------------------
    # Supervisor Information
    # ----------------------------------------------
    with st.expander(
        "🧠 Supervisor Plan",
        expanded=True,
    ):
        supervisor_reasoning = result.get(
            "supervisor_reasoning",
            "No supervisor reasoning was returned.",
        )

        st.markdown(str(supervisor_reasoning))

        selected_agents = result.get(
            "selected_agents",
            [],
        )

        st.write("**Selected agents:**")

        if selected_agents:
            st.write(", ".join(map(str, selected_agents)))
        else:
            st.write("No agent selection was returned.")

    # ----------------------------------------------
    # Flight, Hotel, Weather and Budget
    # ----------------------------------------------
    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):
            st.subheader("✈️ Flight Details")

            flight_results = result.get(
                "flight_results",
                "",
            )

            if flight_results:
                st.markdown(str(flight_results))
            else:
                st.caption("No flight results available.")

        with st.container(border=True):
            st.subheader("🌦️ Weather Information")

            weather_results = result.get(
                "weather_results",
                "",
            )

            if weather_results:
                st.markdown(str(weather_results))
            else:
                st.caption("No weather results available.")

    with col2:

        with st.container(border=True):
            st.subheader("🏨 Hotel Details")

            hotel_results = result.get(
                "hotel_results",
                "",
            )

            if hotel_results:
                st.markdown(str(hotel_results))
            else:
                st.caption("No hotel results available.")

        with st.container(border=True):
            st.subheader("💰 Budget Estimation")

            budget_results = result.get(
                "budget_results",
                "",
            )

            if budget_results:
                st.markdown(str(budget_results))
            else:
                st.caption("No budget results available.")

    # ----------------------------------------------
    # Draft Itinerary
    # ----------------------------------------------
    st.divider()
    st.header("🗺️ Draft Itinerary")

    interrupts = result.get("__interrupt__", [])

    draft = result.get("itinerary", "")

    # An interrupted graph may return the draft in
    # the interrupt payload instead of the state.
    if interrupts:
        interrupt_value = interrupts[0].value

        if isinstance(interrupt_value, dict):
            draft = interrupt_value.get(
                "draft_itinerary",
                draft,
            )

    if draft:
        st.markdown(str(draft))
    else:
        st.info(
            "The graph has not returned a draft itinerary. "
            "Check your itinerary agent and graph state."
        )


# ==================================================
# 8. HUMAN-IN-THE-LOOP APPROVAL
# ==================================================
if st.session_state.waiting_for_approval:

    st.divider()
    st.header("🙋 Human Approval")

    st.write(
        "Review the draft itinerary above. Approve it "
        "or provide feedback to request a revision."
    )

    approved = st.radio(
        "Do you approve this draft?",
        options=[
            "Yes, approve",
            "No, revise it",
        ],
        horizontal=True,
        key="approval_choice",
    )

    feedback = st.text_area(
        "Revision feedback",
        placeholder=(
            "For example: reduce hotel costs, add more "
            "sightseeing, or avoid long travel times."
        ),
        disabled=(approved == "Yes, approve"),
        key="approval_feedback",
    )

    if st.button(
        "✅ Submit Approval",
        type="primary",
        use_container_width=True,
    ):

        is_approved = approved == "Yes, approve"

        if not is_approved and not feedback.strip():
            st.warning(
                "Please enter feedback describing the "
                "changes you want."
            )

        else:
            resume_value = {
                "approved": is_approved,
                "feedback": feedback.strip(),
            }

            try:
                with st.spinner(
                    "Resuming the travel planning workflow..."
                ):
                    final_result = app.invoke(
                        Command(resume=resume_value),
                        config=config,
                    )

                st.session_state.latest_result = final_result

                # Keep approval active if the graph
                # interrupts again for another review.
                st.session_state.waiting_for_approval = (
                    "__interrupt__" in final_result
                )

                st.rerun()

            except Exception as exc:
                st.error(
                    "Unable to resume the approval workflow."
                )
                st.exception(exc)


# ==================================================
# 9. DISPLAY FINAL TRAVEL PLAN
# ==================================================
final_result = st.session_state.latest_result

if (
    final_result
    and final_result.get("final_response")
):

    st.divider()
    st.header("🎉 Final Travel Plan")

    st.markdown(
        str(final_result["final_response"])
    )

    # ----------------------------------------------
    # Download Final Plan
    # ----------------------------------------------
    st.download_button(
        label="⬇️ Download Travel Plan",
        data=str(final_result["final_response"]),
        file_name="travel_plan.md",
        mime="text/markdown",
        use_container_width=True,
    )

elif (
    final_result
    and not st.session_state.waiting_for_approval
    and not final_result.get("final_response")
):
    st.info(
        "The graph returned a result, but no final response "
        "was found. Check the final_response state key in graph.py."
    )


# ==================================================
# 10. FOOTER
# ==================================================
st.divider()

st.caption(
    "Powered by Streamlit, LangChain, and LangGraph. "
    "Verify flight availability, hotel rates, and travel "
    "requirements with the relevant providers before booking."
)
