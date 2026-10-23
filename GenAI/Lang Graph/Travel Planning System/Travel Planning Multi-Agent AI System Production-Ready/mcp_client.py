import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import (AVIATION_STACK_API_KEY,OPENWEATHER_API_KEY,TAVILY_API_KEY)

# ---------------------------------------------------------
# Configure MCP servers
# ---------------------------------------------------------

client = MultiServerMCPClient(
    {
        # Tavily MCP server
        "tavily": {
            "transport": "streamable_http",
            "url": (
                "https://mcp.tavily.com/mcp/"
                f"?tavilyApiKey={TAVILY_API_KEY}"
            ),
        },

        # AviationStack MCP server
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

        # Custom Weather MCP server
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

# Cache tools so we don't load them repeatedly
_tools_cache = None


async def get_tools():
    global _tools_cache

    if _tools_cache is None:
        try:
            _tools_cache = await client.get_tools()

        except Exception as e:
            print("\n========== FULL ERROR ==========")
            print(type(e))
            print(repr(e))

            if hasattr(e, "exceptions"):
                print("\nSUB EXCEPTIONS:")
                for i, sub in enumerate(e.exceptions):
                    print(f"\n--- Exception {i+1} ---")
                    print(type(sub))
                    print(repr(sub))

            raise

    return _tools_cache

async def call_tool(tool_name: str, args: dict = None):
    tools = await get_tools()

    tool = next(
        (tool for tool in tools if tool.name == tool_name),
        None,
    )

    if tool is None:
        raise ValueError(f"Tool '{tool_name}' not found")

    return await tool.ainvoke(args or {})


# ------------------------
# Tavily MCP Tools
# ------------------------



async def tavily_search(query: str):
    return await call_tool("tavily_search", {"query": query})


async def list_airports(search: str = "", limit: int = 10):
    return await call_tool("list_airports", {"search": search, "limit": limit, "offset": 0})


async def list_airlines(search: str = "", limit: int = 10):
    return await call_tool("list_airlines", {"search": search, "limit": limit, "offset": 0})


async def current_weather(city: str):
    return await call_tool("get_current_weather", {"city": city})


async def forecast(city: str):
    return await call_tool("get_forecast", {"city": city})

if __name__ == "__main__":
    import asyncio

    async def main():
        tools = await get_tools()

        print("\nAvailable MCP tools:")
        for tool in tools:
            print(f"- {tool.name}")

    asyncio.run(main())