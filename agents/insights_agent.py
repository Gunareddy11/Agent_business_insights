import os
import requests
from dotenv import load_dotenv, find_dotenv

# Load .env
_ = load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  # Your Groq model

def generate_insights(summary_stats, charts_info):
    """
    Generates AI business insights using Groq API (OpenAI-compatible endpoint)
    """
    prompt = (
        f"Summary Stats: {summary_stats}\n"
        f"Charts Info: {charts_info}\n"
        "Provide clear, actionable business insights."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful business insights assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Extract the output from the OpenAI-compatible response
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating insights: {e}"
