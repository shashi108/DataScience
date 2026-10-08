import random
from fastmcp import FastMCP


# Create a FastMCP server
mcp = FastMCP(name="Demo Server")


# Tool 1: Roll Dice
@mcp.tool
def roll_dice(n_dice: int = 1) -> list[int]:
    """Roll n_dice 6-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]


# Tool 2: Add Two Numbers
@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


# Start the MCP server
if __name__ == "__main__":
    mcp.run()