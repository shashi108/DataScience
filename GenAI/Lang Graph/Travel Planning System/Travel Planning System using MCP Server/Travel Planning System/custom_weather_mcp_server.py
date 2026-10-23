
# Install packages:
# pip install "mcp[cli]" requests python-dotenv

from mcp.server.fastmcp import FastMCP
import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Log to stderr, not stdout (important for MCP stdio)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("Weather Server")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """Get the current weather for a city."""

    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY is missing"}

    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
            },
            timeout=15,
        )

        data = response.json()

        if response.status_code != 200:
            return {
                "error": data.get("message", "Weather API error")
            }

        return {
            "city": data["name"],
            "temperature_c": data["main"]["temp"],
            "feels_like_c": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

    except requests.RequestException as e:
        logger.exception("Current weather request failed")
        return {"error": str(e)}


@mcp.tool()
def get_forecast(city: str) -> dict:
    """Get the next five forecast entries for a city."""

    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY is missing"}

    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
            },
            timeout=15,
        )

        data = response.json()

        if response.status_code != 200:
            return {
                "error": data.get("message", "Forecast API error")
            }

        forecast = []

        for item in data["list"][:5]:
            forecast.append({
                "datetime": item["dt_txt"],
                "temperature_c": item["main"]["temp"],
                "weather": item["weather"][0]["description"],
            })

        return {
            "city": data["city"]["name"],
            "forecast": forecast,
        }

    except requests.RequestException as e:
        logger.exception("Forecast request failed")
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
