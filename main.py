from fastapi import FastAPI
import random
import openai
import json
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:5173"
]

class Request(BaseModel):
    data: str

CHAT_KEY = os.environ.get('CHAT_KEY')
openai.api_key = CHAT_KEY 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"welcome": "this is the main page"}


@app.post('/chat/')
async def chat(payload: Request):
    payload_dict = dict(payload)
    chat = payload_dict['data']
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": chat}
      ]
    )
    return response.choices[0].message.content


@app.get("/random/{limit}")
async def get_random(limit: int):
    rn = random.randint(0, limit)
    return {"number": rn, "limit": limit}
