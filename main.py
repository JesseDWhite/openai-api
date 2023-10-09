from fastapi import FastAPI
import random
import openai
import json
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "https://job-tracker-2b6b1--alpha-preview-ipt58qtt.web.app"
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


@app.post('/{user_token}/extract_keywords/')
async def resume_keywords(payload: Request, user_token: str):
    if (user_token):
        payload_dict = dict(payload)
        request = payload_dict['data']
        task = f'your task is to extract a list of hard skills and soft skills from a block of text in 550 words or less. It needs to be returned as an array in a json object with hard_skills and soft_skills as keys.'
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=750,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message.content


@app.post('/{user_token}/interview_prep/')
async def interview_prep(payload: Request, user_token: str):
    if (user_token):
        payload_dict = dict(payload)
        job_description = payload_dict['data']
        task = f'your task is to create 10 interview questions based on the job description provided in 550 words or less. The job description will be in the form of a block of text. It needs to be returned as an array in a json object with interview_prep as the key.'
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=750,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": job_description}
            ]
        )
        return response.choices[0].message.content


@app.post('/{user_token}/get_score/')
async def interview_prep(payload: Request, user_token: str):
    if (user_token):
        payload_dict = dict(payload)
        job_description = payload_dict['job']
        resume = payload_dict['resume']
        task = f'your task is to provide a score from 0 to 100 based on the qualifications on a resume compared to a job description. The resume and job desciption will be in the form of a block of text within an object.'
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=750,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": job_description}
            ]
        )
        return response.choices[0].message.content


@app.post('/write_cover_letter/')
async def write_cover_letter(payload: Request):
    payload_dict = dict(payload)
    resume = payload_dict['resume']
    job_description = payload_dict['job_description']
    name = payload_dict['name']
    email = payload_dict['email']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        max_tokens=300,
        messages=[
            {"role": "user", "content": ''}
        ]
    )
    return response.choices[0].message.content
