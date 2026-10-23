# Travel Planning System

This directory groups three related AI travel-planning projects built around LangChain/LangGraph workflows and external tool integrations. Each folder explores a different architecture for generating trip itineraries and travel plans.

## Overview of the 3 folders

### 1. Travel Planning Multi-Agent AI System Production-Ready
This is the most complete and production-oriented implementation.

It includes:
- a multi-agent supervisor architecture
- specialized agents for flights, hotels, weather, budget, and itinerary planning
- a human approval step before finalizing the final plan
- Streamlit-based web UI
- integrations with external APIs and MCP-based tools
- saved travel plan outputs in a dedicated folder

This project is the best place to start if you want to understand the full multi-agent design.

### 2. Travel Planning System using MCP Server
This project focuses on Model Context Protocol (MCP) integration.

It demonstrates:
- connecting the travel system to external tools/services through MCP
- modular tool access for data like weather or flight information
- a server/client pattern for external service integration
- a more extensible architecture for tool-based planning tasks

This version is useful for learning how AI agents interact with external systems using a standard interface.

### 3. Travel Planning System with Tools
This project uses a tool-driven approach to planning.

It contains:
- a travel planning application and workflow logic
- tool-based interactions for collecting travel data
- a simpler architecture centered on function/tool execution
- separate tools folder for reusable planning capabilities

This version is ideal for understanding a lighter, tool-first implementation of the same travel assistant concept.

## Relationship between the folders

All three folders solve the same core problem: generating a useful travel plan from natural-language user requests. The main difference is the implementation style:

- Multi-Agent AI System Production-Ready: full orchestration and supervisor-agent architecture
- Using MCP Server: external tool integration using MCP
- With Tools: tool-calling based workflow design

## Suggested reading order

1. Start with `Travel Planning System with Tools`  
2. Study `Travel Planning System using MCP Server`
3. Review `Travel Planning Multi-Agent AI System Production-Ready`

## Typical workflow across the projects

- User provides a trip request
- The planner identifies relevant travel constraints
- AI agents or tools fetch required information
- Travel data is combined into a local draft itinerary
- Final output is refined into a usable trip plan

## Notes

These folders are related versions of the same idea rather than unrelated projects. They showcase different ways of building a travel-planning assistant with frontier AI, external tools, and workflow orchestration.
