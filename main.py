from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/")
async def root():
    return {"welcome": "this is the main page"}


@app.get("/random")
async def get_random():
    rn = random.randint(0, 1000)
    return {"number": rn, "limit": 1000}


@app.get("/random/{limit}")
async def get_random(limit: int):
    rn = random.randint(0, limit)
    return {"number": rn, "limit": limit}
