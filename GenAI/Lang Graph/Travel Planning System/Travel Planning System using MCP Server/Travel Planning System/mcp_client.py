
import os
import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv(override=True)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

# ---------------------------------------------------------
# Configure MCP servers
# ---------------------------------------------------------

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": (
                "https://mcp.tavily.com/mcp/"
                f"?tavilyApiKey={TAVILY_API_KEY}"
            ),
        },

        "aviationstack": {
            "transport": "stdio",
            "command": (
                "/Volumes/E/Self Study Agentic AI/Lang Graph/"
                "Travel Planning System/aviationstack-mcp/"
                ".venv/bin/python"
            ),
            "args": [
                "-m",
                "aviationstack_mcp",
                "mcp",
                "run",
            ],
            "env": {
                "AVIATIONSTACK_API_KEY": AVIATION_STACK_API_KEY,
            },
        },

        "weather": {
            "transport": "stdio",
            "command": (
                "/Volumes/E/Self Study Agentic AI/Lang Graph/"
                "Travel Planning System/planner_env/bin/python"
            ),
            "args": [
                "/Volumes/E/Self Study Agentic AI/Lang Graph/"
                "Travel Planning System/custom_weather_mcp_server.py"
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
            },
        },
    }
)

# ---------------------------------------------------------
# MCP tool initialization
# ---------------------------------------------------------

search_tool = None
aviation_tools = {}
weather_tool = None
forecast_tool = None
initialization_lock = asyncio.Lock()


async def initialize_mcp():
    global search_tool, aviation_tools
    global weather_tool, forecast_tool

    async with initialization_lock:
        if (
            search_tool is not None
            and aviation_tools
            and weather_tool is not None
            and forecast_tool is not None
        ):
            return

        tools = await client.get_tools()

        print("\nAvailable MCP tools:")
        for tool in tools:
            print(f"- {tool.name}")

        tool_map = {tool.name: tool for tool in tools}

        # Tavily
        search_tool = tool_map.get("tavily_search")

        # Weather
        weather_tool = tool_map.get("get_current_weather")
        forecast_tool = tool_map.get("get_forecast")

        # AviationStack
        aviation_tools = {
            name: tool
            for name, tool in tool_map.items()
            if name not in {
                "tavily_search",
                "get_current_weather",
                "get_forecast",
            }
        }

        if search_tool is None:
            raise RuntimeError(
                "Tool 'tavily_search' was not discovered. "
                "Check the actual Tavily tool names above."
            )

        if weather_tool is None or forecast_tool is None:
            raise RuntimeError(
                "Weather tools were not discovered. "
                "Check the Weather MCP server."
            )


# ---------------------------------------------------------
# Search / hotel research
# ---------------------------------------------------------

async def tavily_mcp_search(query: str):
    await initialize_mcp()
    return await search_tool.ainvoke({"query": query})


# ---------------------------------------------------------
# Flight tools
# ---------------------------------------------------------

async def aviation_mcp_call(
    tool_name: str,
    tool_args: dict | None = None,
):
    await initialize_mcp()

    tool = aviation_tools.get(tool_name)

    if tool is None:
        raise ValueError(
            f"Aviation tool '{tool_name}' not found. "
            f"Available tools: {list(aviation_tools)}"
        )

    return await tool.ainvoke(tool_args or {})


# ---------------------------------------------------------
# Weather
# ---------------------------------------------------------

async def weather_mcp_search(city: str):
    await initialize_mcp()
    return await weather_tool.ainvoke({"city": city})


async def forecast_mcp_search(city: str):
    await initialize_mcp()
    return await forecast_tool.ainvoke({"city": city})


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=GROQ_API_KEY,
    temperature=0,
)


# ---------------------------------------------------------
# Destination extractor
# ---------------------------------------------------------

def extract_destination(query: str) -> str:
    prompt = f"""
Extract only the destination city or country from the query.
If no destination is mentioned, return NONE.
Query: {query}
Return only the destination name.
"""

    response = llm.invoke(prompt)
    return response.content.strip()


# ---------------------------------------------------------
# Main: test MCP tools
# ---------------------------------------------------------

async def main():
    await initialize_mcp()

    print("\nTesting destination extraction:")
    print(extract_destination("Plan a 7-day trip to Tokyo"))

    # Uncomment to test individual tools after discovery:
    # print(await tavily_mcp_search("best hotels in Tokyo"))
    # print(await weather_mcp_search("Tokyo"))
    # print(await forecast_mcp_search("Tokyo"))


if __name__ == "__main__":
    asyncio.run(main())
