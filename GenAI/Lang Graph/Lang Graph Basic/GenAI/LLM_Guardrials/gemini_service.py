from google import genai
from config import (GEMINI_API_KEY, GEMINI_MODEL)

# Initialize the Gemini client with the API key
client = genai.Client(api_key=GEMINI_API_KEY)
def generate_response(prompt:str) -> str:
    """
    Generate a response from the Gemini model based on the provided prompt.
    Args:prompt (str): The input prompt for the model.
    Returns:str: The generated response from the Gemini model.
    """
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response.text 

#print(generate_response("Hello, how are you?"))