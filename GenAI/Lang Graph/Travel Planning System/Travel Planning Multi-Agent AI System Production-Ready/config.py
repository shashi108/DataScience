
import os
from pathlib import Path
from dotenv import load_dotenv
#from langchain_groq import ChatGroq
#local ollama
from langchain_ollama import ChatOllama

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

print("Env file exists:", ENV_FILE.exists())
print("AviationStack key loaded:", bool(AVIATION_STACK_API_KEY))

                          

def get_llm():
    #return ChatGroq(model="openai/gpt-oss-120b",api_key=GROQ_API_KEY, temperature=0)
    return ChatOllama(model="qwen3:1.7b",temperature=0)
response = get_llm().invoke("the capital of India? in one word")
print(response.content)
