1| # Travel Planning Multi-Agent AI System
2| 
3| A production-ready multi-agent travel planning application built with Python, LangGraph, LangChain, and Streamlit. The system coordinates specialized agents for flights, hotels, weather, budgeting, and itinerary generation to create structured trip plans from natural language requests.
4| 
5| ## Overview
6| 
7| This project allows a user to describe a trip in plain English and receive a structured draft itinerary with supporting reasoning from multiple AI agents. It follows a human-in-the-loop workflow:
8| 
9| 1. A supervisor validates the request.
10| 2. Relevant specialist agents are selected.
11| 3. Agents gather and analyze travel information.
12| 4. A draft itinerary is generated.
13| 5. Human approval is requested.
14| 6. A final polished trip plan is created.
15| 
16| The application is designed for experimentation, prototyping, and local deployment using open-source or cloud-based LLM backends.
17| 
18| ## Key Features
19| 
20| - Multi-agent orchestration with LangGraph
21| - Specialist travel agents for:
22|   - flight planning
23|   - hotel and stay recommendations
24|   - weather analysis
25|   - budget assessment
26|   - final itinerary generation
27| - Human approval step before final plan delivery
28| - Integration with Tavily search, aviation APIs, and weather APIs
29| - Streamlit-based interactive user interface
30| - Supports local and cloud LLM providers
31| - Saves generated travel plans in the `travel_plans/` directory
32| 
33| ## Architecture
34| 
35| The system is structured around a LangGraph workflow where a supervisor routes work to specialist agents. Each agent works on its domain and contributes results to a shared state object that is used to build the final trip plan.
36| 
37| Core workflow components:
38| 
39| - `app.py` — main Streamlit UI
40| - `app2.py` — alternate app implementation
41| - `agents.py` — agent definitions and orchestration logic
42| - `graph.py` — workflow graph construction
43| - `state.py` — graph state schema
44| - `config.py` — environment configuration and LLM setup
45| - `mcp_client.py` — MCP integrations for external tools and data sources
46| - `weather_mcp_server.py` — weather tool server
47| 
48| ## Project Structure
49| 
| 50| ```text
51| Travel Planning Multi-Agent AI System Production-Ready/
52| ├── app.py                          # Main Streamlit application
53| ├── app2.py                         # Alternative app entry point
54| ├── agents.py                       # Agent logic and workflow behavior
55| ├── config.py                      # LLM and environment configuration
56| ├── graph.py                       # LangGraph graph definition
57| ├── state.py                       # Travel workflow state schema
58| ├── mcp_client.py                  # MCP client and API integrations
59| ├── weather_mcp_server.py          # Weather MCP server
60| ├── requirements.txt               # Python dependencies
61| ├── planner_env_new/               # Additional workflow/environment assets
62| ├── travel_plans/                  # Generated travel plans
63| ├── Multi-Agent Travel Planning Workflow.png
64| ├── Supervisor Agent Travel Flowchart.png
65| ├── Supervisor Agent Travel Workflow.png
66| ├── Travel Planning Multi-Agent Architecture.png
67| ├── README.md
68| ├── .env                          # Local environment file (not always committed)
69| ├── .venv                         # Optional local virtual environment
70| └── .gitignore                    # Git ignore configuration (if present)
71| ```
72| 
73| ## Tech Stack
74| 
75| - Python 3.10+
76| - LangGraph
77| - LangChain
78| - LangChain Community
79| - Streamlit
80| - Ollama / Groq for LLM inference
81| - Tavily Search
82| - Aviation Stack API
83| - OpenWeather API
84| - PostgreSQL (optional checkpoint support)
85| 
86| ## Prerequisites
87| 
88| Before running the project, ensure you have:
89| 
90| - Python 3.10 or newer
91| - `pip` installed
92| - `git` installed
93| - Optional: PostgreSQL if using checkpointing or database-backed state
94| - Optional: Ollama installed locally for local model inference
95| 
96| ## Environment Setup
97| 
98| Create a `.env` file in this directory with the required variables:
99| 
100| ```bash
101| GROQ_API_KEY=your_groq_key
102| TAVILY_API_KEY=your_tavily_key
103| AVIATIONSTACK_API_KEY=your_aviationstack_key
104| OPENWEATHER_API_KEY=your_openweather_key
105| DATABASE_URL=postgresql://user:password@host:5432/dbname
106| ```
107| 
108| The project loads environment variables from the same folder using `python-dotenv`.
| 109| 
110| If you are using Ollama locally, install and pull the model:
111| 
112| ```bash
113| ollama pull qwen3:1.7b
114| ```
115| 
116| ## Installation
117| 
118| From the repository root:
119| 
120| ```bash
121| cd "GenAI/Lang Graph/Travel Planning System/Travel Planning Multi-Agent AI System Production-Ready"
122| python -m venv .venv
123| source .venv/bin/activate   # Windows: .venv\Scripts\activate
124| pip install -r requirements.txt
125| ```
126| 
127| ## PostgreSQL Setup (Optional but Recommended)
128| 
129| If you want to enable PostgreSQL-backed state or LangGraph checkpointing, set up a local database first:
130| 
131| ```bash
132| # macOS (Homebrew)
133| brew install postgresql
134| brew services start postgresql
135| 
| 136| # Ubuntu / Debian
137| sudo apt update
138| sudo apt install postgresql postgresql-contrib
139| sudo -u postgres psql -c "CREATE DATABASE travel_planner;"
140| sudo -u postgres psql -d travel_planner -c "CREATE USER travel_user WITH ENCRYPTED PASSWORD 'your_password';"
141| sudo -u postgres psql -d travel_planner -c "GRANT ALL PRIVILEGES ON DATABASE travel_planner TO travel_user;"
142| ```
143| 
144| Then add the connection string to your `.env` file:
145| 
146| ```bash
147| DATABASE_URL=postgresql://travel_user:your_password@localhost:5432/travel_planner
148| ```
149| 
150| If you are not using PostgreSQL checkpointing, you can leave `DATABASE_URL` unset or empty.
151| 
152| ## Run the Application
153| 
154| Start the main Streamlit app:
155| 
155| ```bash
156| streamlit run app.py
157| ```
158| 
159| This launches the travel planner interface where users can:
160| 
161| - enter a trip request
162| - generate a draft itinerary
163| - review specialist agent findings
164| - approve or revise the plan
165| - save the final output as a Markdown travel plan
166| 
167| ## Example Use
168| 
169| ```text
170| Plan a 7-day trip to Japan under ₹2 lakh. Include flights, hotel suggestions, weather, budget analysis, and a sightseeing itinerary.
171| ```
172| 
173| ## Workflow Summary
174| 
175| 1. User enters a travel request.
176| 2. Supervisor validates the request and selects relevant agents.
177| 3. Flight, hotel, weather, and budget agents gather information.
178| 4. Itinerary agent creates a draft travel plan.
179| 5. Human approval is requested.
180| 6. Final response agent generates the final polished plan.
181| 
182| ## Notes
183| 
184| - Some features depend on external APIs and valid keys.
185| - The default configuration in `config.py` uses Ollama with `qwen3:1.7b`.
186| - You can switch to Groq by uncommenting the Groq configuration block.
187| - Generated plans are saved under the `travel_plans/` directory.
188| - This project is primarily intended for learning, prototyping, and experimentation.
189| 
190| ## License
191| 
192| This project is provided as-is for learning and experimentation. If you plan to publish, redistribute, or commercialize it, check whether a project-specific license or attribution requirement applies to the original data sources and APIs you use.
193| 
194| ## Author
195| 
196| Shashi Kumar
197| 