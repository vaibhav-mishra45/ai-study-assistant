from google import genai
from dotenv import load_dotenv
import os
from rich import print
from rich.console import Console

console = Console()
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_response(prompt):
    """Sends a prompt to Gemini and returns the generated response."""
    with console.status("Thinking..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        except Exception as e:
            print(f"[red]Error generating response: {e}[/red]")
            return (
                "Unable to connect to Gemini. "
                "Please check your internet connection or try again later."
            )
    return response.text