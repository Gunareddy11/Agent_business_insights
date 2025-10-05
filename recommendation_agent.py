# File: agents/recommendation_agent.py
import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  # Your Groq model

def generate_recommendations(insights: str) -> str:
    """
    Generate 3 actionable business recommendations based on AI insights.
    """
    prompt = f"""
    You are a business consultant AI.
    Based on these insights:
    {insights}
    Suggest 3 actionable business recommendations.
    """

    # OpenAI-compatible Groq API endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful business consultant AI."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Extract the text output from OpenAI-compatible response
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating recommendations: {e}"
