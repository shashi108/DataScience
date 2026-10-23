""" check message in db
SELECT
    thread_id,
    checkpoint_id,
    checkpoint_ns,
    checkpoint -> 'channel_values' AS channel_values,
    metadata
FROM public.checkpoints
ORDER BY checkpoint_id DESC
"""
#------------------------------------------------------------------
import os
import uuid
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from graph import app

st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #080d14;
}

/* ── Hero ── */
.hero-wrapper {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 2rem;
    height: 280px;
}
.hero-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.35);
    position: absolute;
    top: 0; left: 0;
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}
.hero-badge {
    background: rgba(58,123,213,0.25);
    border: 1px solid rgba(58,123,213,0.5);
    color: #7ab8f5 !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 0.9rem;
    display: inline-block;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.6rem;
    line-height: 1.2;
}
.hero-sub {
    color: #94adc8;
    font-size: 1rem;
    max-width: 560px;
}

/* ── Input card ── */
.input-card {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
}
.input-label {
    color: #7ab8f5;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Quick destinations ── */
.dest-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 1.2rem;
}
.dest-chip {
    background: #111b2b;
    border: 1px solid #1e3050;
    color: #f7fdf4;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
}
.dest-chip:hover { background: #1a2e47; border-color: #3a7bd5; color: #fff; }

/* ── Generate button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(26,107,191,0.35), 0 4px 15px rgba(0,0,0,0.4) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 40px rgba(26,107,191,0.6), 0 6px 20px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] {
    background: #0e1a2e !important;
    border: 1px solid #1e3050 !important;
    border-radius: 12px !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: #0e1a2e !important;
    border-radius: 12px 12px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: #0a1520 !important;
    color: #ffffff !important;
    padding: 0.25rem 0.5rem !important;
}
[data-testid="stStatusWidget"] * { color: #ffffff !important; }
[data-testid="stStatusWidget"] a { color: #4ea8f0 !important; }
[data-testid="stStatusWidget"] hr { border-color: #1e3050 !important; }

/* ── Section headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2e44;
}
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e0edf8; }

/* ── Metric bar ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #4ea8f0; }
.metric-lbl { font-size: 0.78rem; color: #5a7a96; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Final plan ── */
.final-card {
    background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3a5c;
    border-left: 4px solid #3a7bd5;
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #cce0f5;
    font-size: 0.95rem;
}

/* ── Save bar ── */
.save-bar {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #5a8ab0;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid #141f30 !important;
}
.sidebar-chip {
    background: #0e1a2b;
    border: 1px solid #1a2e44;
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.83rem;
    color: #7aa8cc;
}
.sidebar-title { color: #e0edf8; font-size: 1rem; font-weight: 600; margin: 1rem 0 0.5rem; }

/* Hide branding */
#MainMenu, footer, header { visibility: hidden; }

/* Textarea */
.stTextArea textarea {
    background: #0a1520 !important;
    border: 1px solid #1e2e44 !important;
    border-radius: 10px !important;
    color: #e8f4ff !important;
    font-size: 0.95rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}
.stTextArea textarea::placeholder { color: #4a6a85 !important; }

/* Text input (sidebar User ID field) */
input[type="text"], .stTextInput input {
    background: #0e1a2b !important;
    border: 1px solid #1a2e44 !important;
    border-radius: 8px !important;
    color: #e0edf8 !important;
}
input[type="text"]:focus, .stTextInput input:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}
input[type="text"]::placeholder { color: #3a5570 !important; }

/* All Streamlit labels — dark bg → light text */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label {
    color: #7ab8f5 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
}

/* General markdown / paragraph text */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #cce0f5 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e8f4ff !important; }
.stMarkdown code {
    background: #0e1a2b !important;
    color: #7ab8f5 !important;
    padding: 0.15em 0.4em;
    border-radius: 4px;
}

/* Metric labels — was #5a7a96 (too dim on dark bg) */
.metric-lbl { color: #7aa8cc !important; }

/* Save bar — was #5a8ab0 (slightly dim) */
.save-bar { color: #8ab8d8 !important; }
.save-bar code { color: #7ab8f5 !important; background: #0a1520 !important; }

/* Streamlit warning / info / success on dark bg */
.stAlert { background: #0e1a2b !important; border-radius: 10px !important; }
.stAlert p, .stAlert div { color: #e0edf8 !important; }

/* Sidebar text & dividers */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown { color: #a0c4e0 !important; }
section[data-testid="stSidebar"] hr { border-color: #1a2e44 !important; }

/* Download button — light bg → dark text  */
div[data-testid="stDownloadButton"] > button {
    background: #1a3a5c !important;
    color: #e8f4ff !important;
    border: 1px solid #2a5080 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar / Session ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 Shashi Travel Planner</div>", unsafe_allow_html=True)
    st.markdown("---")
    user_id = st.text_input("👤 User ID", value="Shashi Kumar", key="user_id")
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"

    if st.button("➕ New Thread", use_container_width=True):
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
        st.session_state.pop("latest_result", None)
        st.session_state.pop("waiting_for_approval", None)
        st.session_state.pop("current_query", None)
        st.rerun()

    st.caption(f"Thread: {st.session_state.thread_id}")
    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in ["🔗 LangGraph", "🧠 Ollama", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    for step in ["① Flight Agent", "② Hotel Agent", "③ Weather Agent","④ Budget Agent", "⑤ Itinerary Agent","⑥ Final Response Agent"]:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)   
# Keep the thread associated with the current user ID when the ID changes.
if not st.session_state.thread_id.startswith(f"{user_id}_"):
    st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈️ AI Travel Booking System</div>
        <div class="hero-sub">Plan your trip with specialized agents for flights, hotels, weather, budget, and itinerary generation.</div>
    </div>
</div>
""", unsafe_allow_html=True)

DESTINATIONS = [
    ("🇮🇳 Bengaluru", "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=300&q=70"),
    ("🇮🇳 Mumbai", "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=300&q=70"),
    ("🇮🇳 Delhi", "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=300&q=70"),
    ("🇮🇳 Chennai", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=300&q=70"),
    ("🇮🇳 Kolkata", "https://images.unsplash.com/photo-1558431382-27e303142255?w=300&q=70"),
]
cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:10px;overflow:hidden;position:relative;height:90px;">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.55);" />
            <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;color:#fff;font-size:0.8rem;font-weight:600;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

QUICK = [
    "Plan a 7-day Delhi trip from Bengaluru under ₹50,000",
    "Plan a 5-day Mumbai trip under ₹40,000",
    "Plan a 3-day Bengaluru trip under ₹25,000",
]
quick_cols = st.columns(len(QUICK))
for i, (qc, prompt) in enumerate(zip(quick_cols, QUICK)):
    with qc:
        if st.button(prompt, key=f"quick_{i}", use_container_width=True):
            st.session_state.travel_query = prompt

query = st.text_area(
    "Travel request",
    value=st.session_state.get("travel_query", ""),
    placeholder="Plan a 7-day Japan trip under ₹2 lakh. Include flights, hotels, weather, budget, and sightseeing.",
    height=110,
    key="travel_query",
)

if st.button("🚀 Create Draft Plan", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Please describe your trip first.")
    else:
        st.session_state.current_query = query
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "user_id": user_id,
            "user_query": query,
            "flight_results": "",
            "hotel_results": "",
            "weather_results": "",
            "budget_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }
        try:
            with st.spinner("Agents are planning your trip..."):
                result = app.invoke(initial_state, config=config)
            st.session_state.latest_result = result
            st.session_state.waiting_for_approval = "__interrupt__" in result
        except Exception as exc:
            st.error(f"Could not generate the draft. Check that your graph state and compiled app support these fields and interrupts. Details: {exc}")

result = st.session_state.get("latest_result")

def show_value(state, key, fallback=""):
    value = state.get(key, fallback)
    if isinstance(value, list):
        return "\n\n".join(str(item) for item in value)
    return value if value is not None else ""

if result:
    st.markdown("<div class='sec-head'><span>🤖 Supervisor Plan</span></div>", unsafe_allow_html=True)
    reasoning = show_value(result, "supervisor_reasoning")
    if reasoning:
        st.markdown(reasoning)
    selected_agents = result.get("selected_agents", [])
    if selected_agents:
        st.write("**Selected agents:**", ", ".join(map(str, selected_agents)))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✈️ Flight")
        st.markdown(show_value(result, "flight_results") or "_No flight information returned._")
        st.subheader("🌦️ Weather")
        st.markdown(show_value(result, "weather_results") or "_No weather information returned._")
    with col2:
        st.subheader("🏨 Hotels")
        st.markdown(show_value(result, "hotel_results") or "_No hotel information returned._")
        st.subheader("💰 Budget")
        st.markdown(show_value(result, "budget_results") or "_No budget information returned._")

    st.markdown("<div class='sec-head'><span>🗓️ Draft Itinerary</span></div>", unsafe_allow_html=True)
    interrupt_data = result.get("__interrupt__", [])
    draft = ""
    if interrupt_data:
        interrupt_value = getattr(interrupt_data[0], "value", {})
        if isinstance(interrupt_value, dict):
            draft = interrupt_value.get("draft_itinerary", "")
    draft = draft or show_value(result, "itinerary")
    st.markdown(draft or "_No draft itinerary returned._")

    # Approval is shown only when the graph returned an interrupt.
    if st.session_state.get("waiting_for_approval"):
        st.divider()
        st.subheader("🧑‍⚖️ Human Approval")
        approved = st.radio(
            "Approve this draft?",
            ["Yes", "No, revise it"],
            horizontal=True,
            key="approval_choice",
        )
        feedback = st.text_area(
            "Feedback / requested revisions",
            disabled=(approved == "Yes"),
            key="approval_feedback",
            placeholder="Tell the agents what should change...",
        )
        if st.button("Submit Approval", type="primary"):
            try:
                with st.spinner("Resuming the workflow..."):
                    final_result = app.invoke(
                        Command(resume={
                            "approved": approved == "Yes",
                            "feedback": feedback,
                        }),
                        config=config,
                    )
                st.session_state.latest_result = final_result
                st.session_state.waiting_for_approval = "__interrupt__" in final_result
                st.rerun()
            except Exception as exc:
                st.error(f"Could not resume the workflow. Ensure the graph uses an interrupt and a checkpointer. Details: {exc}")

    final_result = st.session_state.get("latest_result")
    final_text = show_value(final_result, "final_response") if final_result else ""
    if not final_text and final_result:
        messages = final_result.get("messages", [])
        if messages:
            last_message = messages[-1]
            final_text = getattr(last_message, "content", "") or (last_message.get("content", "") if isinstance(last_message, dict) else "")

    if final_text and not st.session_state.get("waiting_for_approval"):
        st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='final-card'>{final_text}</div>", unsafe_allow_html=True)

        # Download a portable Markdown copy of the completed plan.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        file_content = f"""# Travel Plan

**Request:** {st.session_state.get('current_query', query)}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**User ID:** {user_id}
**Thread ID:** {st.session_state.thread_id}

## Supervisor reasoning
{reasoning or 'N/A'}

## Selected agents
{', '.join(map(str, selected_agents)) if selected_agents else 'N/A'}

## Flights
{show_value(final_result, 'flight_results') or 'N/A'}

## Hotels
{show_value(final_result, 'hotel_results') or 'N/A'}

## Weather
{show_value(final_result, 'weather_results') or 'N/A'}

## Budget
{show_value(final_result, 'budget_results') or 'N/A'}

## Itinerary
{show_value(final_result, 'itinerary') or draft or 'N/A'}

## Final travel plan
{final_text}
"""
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as file:
            file.write(file_content)

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button(
                "⬇️ Download Plan",
                data=file_content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )
        with info_col:
            st.markdown(
                f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                unsafe_allow_html=True,
            )
