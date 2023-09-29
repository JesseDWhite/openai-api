from fastapi import FastAPI
import random
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

CHAT_KEY = os.getenv('CHAT_KEY')
openai.api_key = CHAT_KEY 
app = FastAPI()


@app.get("/")
async def root():
    return {"welcome": "this is the main page"}


@app.get('/chat/{name}')
async def chat(name: str):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": f'Hey this is {name}, let me know if this is connected.'}
      ]
    )
    return response.choices[0].message.content


@app.get("/random/{limit}")
async def get_random(limit: int):
    rn = random.randint(0, limit)
    return {"number": rn, "limit": limit}
