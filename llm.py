import os

from openai import OpenAI
from config import OPENAI_API_KEY

# OPENAI_BASE_URL env is honored by the client automatically (e.g. OpenRouter);
# LLM_MODEL picks the model to match the provider.
client = OpenAI(api_key=OPENAI_API_KEY)
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

def generate_followup_message(name, description):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a motivational fitness coach and nutrition expert."},
            {"role": "user", "content": f"Generate a short, personalized message for {name}. Context: {description}"}
        ]
    )
    return response.choices[0].message.content