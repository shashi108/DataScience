"""
1. **Import Required Libraries**
2. **Configure MCP Server**
3. **Create MCP Client**
4. **Discover MCP Tools**
5. **Create Tool Dictionary**
6. **Create Ollama LLM**
7. **Bind MCP Tools to LLM**
8. **Send User Request**
9. **LLM Requests Tool**
10. **Execute MCP Tool**
11. **Return Tool Result**
12. **Send Result Back to LLM**
13. **Generate Final Response**
14. **Display Final Answer**

"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import asyncio
import json

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Server Configuration information

SERVERS = {
    #Local Server
    "Demo Server": {
      "command": "/opt/anaconda3/bin/uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/Users/shashi/Desktop/MCP Demo/main.py"
      ],
      "env": {},
      "transport": "stdio"
    }
    #Remove server
    # "Remote": {
        # "transport": "streamable_http",
        # "url": "https://shashi-demo-remote-server.fastmcp.app/mcp",
    # }
}

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
async def main():

    # 1. Create MCP client
    client = MultiServerMCPClient(SERVERS)

    # 2. Get tools from all MCP servers
    tools = await client.get_tools()

    # 3. Create tool dictionary
    named_tools = {
        tool.name: tool
        for tool in tools
    }

    print("\nAvailable tools:")
    for tool_name in named_tools:
        print(f"  - {tool_name}")

    # 4. Create LLM
    llm = ChatOllama(model="qwen3:4b")

    # 5. Bind MCP tools to LLM
    llm_with_tools = llm.bind_tools(tools)

    # 6. User request
    prompt = "add 3 and 6"

    messages = [HumanMessage(content=prompt)]

    # 7. First LLM call
    response = await llm_with_tools.ainvoke(messages)

    print("\nLLM Response:")
    print(response.content)

    # 8. Check whether LLM requested tools
    if not response.tool_calls:
        return

    print("\nTool Calls:")

    tool_messages = []

    # 9. Execute requested MCP tools
    for tc in response.tool_calls:

        tool_name = tc["name"]
        tool_args = tc.get("args") or {}
        tool_call_id = tc["id"]

        print(f"\nTool: {tool_name}")
        print(f"Arguments: {tool_args}")

        if tool_name not in named_tools:
            print(f"Tool not found: {tool_name}")
            continue

        # Execute MCP tool
        result = await named_tools[tool_name].ainvoke(tool_args)

        print(f"Result: {result}")
        tool_messages.append(
            ToolMessage(tool_call_id=tool_call_id,content=json.dumps(result, default=str),)
        )

    # 10. Send tool result back to LLM
    messages.extend([response,*tool_messages ])

    final_response = await llm_with_tools.ainvoke(messages)

    print("\nFinal Response:")
    print(final_response.content)


if __name__ == "__main__":
    asyncio.run(main())