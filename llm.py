from openai import OpenAI
from config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_followup_message(name, description):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a motivational fitness coach and nutrition expert."},
            {"role": "user", "content": f"Generate a short, personalized message for {name}. Context: {description}"}
        ]
    )
    return response.choices[0].message.content