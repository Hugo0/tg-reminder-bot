import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_chiding_message(goal):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a motivational fitness coach."},
            {"role": "user", "content": f"Generate a short, chiding message to remind someone about their exercise goal: {goal}"}
        ]
    )
    return response.choices[0].message.content