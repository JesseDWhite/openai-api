from fastapi import FastAPI
import random
import openai
import json
import os
from pydantic import BaseModel

class Request(BaseModel):
    payload: str

CHAT_KEY = os.environ.get('CHAT_KEY')
openai.api_key = CHAT_KEY 
app = FastAPI()


@app.get("/")
async def root():
    return {"welcome": "this is the main page"}


@app.post('/chat/{payload}')
async def chat(payload: Request):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": payload}
      ]
    )
    return response.choices[0].message.content


@app.get("/random/{limit}")
async def get_random(limit: int):
    rn = random.randint(0, limit)
    return {"number": rn, "limit": limit}
