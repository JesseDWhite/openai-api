from __future__ import print_function
from fastapi import FastAPI
import openai
import json
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from oauth2client import tools
# import googleapiclient.discovery as discovery
from httplib2 import Http

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://job-tracker-2b6b1--alpha-preview-ipt58qtt.web.app",
    "https://job-tracker-2b6b1--alpha-preview-ipt58qtt.web.app/?fbclid=IwAR1mJqo_jBE2a-KvyMAmhtfRbd_HiMzRn5ikev7A2dmOv2EJlLbHjjYptT4",
    "https://nomorecoverletter.com/",
]


class Request(BaseModel):
    data: str


CHAT_KEY = os.environ.get("CHAT_KEY")
openai.api_key = CHAT_KEY
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/{user_token}/extract_keywords/")
async def resume_keywords(payload: Request, user_token: str):
    if user_token:
        payload_dict = dict(payload)
        request = payload_dict["data"]
        task = f"your task is to extract a list of hard skills and soft skills from a block of text in 550 words or less. It needs to be returned as an array in a json object with hard_skills and soft_skills as keys."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=750,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": request},
            ],
        )
        return response.choices[0].message.content


@app.post("/{user_token}/interview_prep/")
async def interview_prep(payload: Request, user_token: str):
    if user_token:
        payload_dict = dict(payload)
        job_description = payload_dict["data"]
        task = f"your task is to create 10 interview questions based on the job description provided in 550 words or less. The job description will be in the form of a block of text. It needs to be returned as an array in a json object with interview_prep as the key."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=750,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": job_description},
            ],
        )
        return response.choices[0].message.content


@app.post("/{user_token}/get_score/")
async def interview_prep(payload: Request, user_token: str):
    if user_token:
        payload_dict = dict(payload)
        job_description = payload_dict["job"]
        resume = payload_dict["resume"]
        task = f"your task is to provide a score from 0 to 100 based on the qualifications on a resume compared to a job description. The resume and job desciption will be in the form of a block of text within an object."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            max_tokens=750,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": job_description},
            ],
        )
        return response.choices[0].message.content


# @app.post("/{user_token}/get_document_text/")
# async def get_document_text(payload: Request, user_token: str):
#     if user_token:
#         payload_dict = dict(payload)
#         document_id = payload_dict["data"]
#         SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

#         creds = None

#         if os.path.exists("token.json"):
#             creds = Credentials.from_authorized_user_file(
#                 "token.json", "credentials.json"
#             )
#             # If there are no (valid) credentials available, let the user log in.
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     "credentials.json", SCOPES
#                 )
#             creds = flow.run_local_server(port=55424)
#         # return creds
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#         try:
#             service = build("docs", "v1", credentials=creds)

#             document = service.documents().get(documentId=document_id).execute()

#             doc = document.get("body").get("content")
#             return read_structural_elements(doc)
#         except HttpError as err:
#             return err


# def read_paragraph_element(element):
#     text_run = element.get("textRun")
#     if not text_run:
#         return ""
#     return text_run.get("content")


# def read_structural_elements(elements):
#     text = ""
#     for value in elements:
#         if "paragraph" in value:
#             elements = value.get("paragraph").get("elements")
#             for elem in elements:
#                 text += read_paragraph_element(elem)
#         elif "table" in value:
#             table = value.get("table")
#             for row in table.get("tableRows"):
#                 cells = row.get("tableCells")
#                 for cell in cells:
#                     text += read_structural_elements(cell.get("content"))
#         elif "tableOfContents" in value:
#             toc = value.get("tableOfContents")
#             text += read_structural_elements(toc.get("content"))
#     return text


# @app.post("/{user_token}/get_document_text/")
# async def get_document_text(payload: Request, user_token: str):
#     if user_token:
#         payload_dict = dict(payload)
#         document_id = payload_dict["data"]

#         credentials = get_credentials()
#         http = credentials.authorize(Http())
#         docs_service = discovery.build(
#             "docs",
#             "v1",
#             http=http,
#             discoveryServiceUrl="https://docs.googleapis.com/$discovery/rest?version=v1",
#         )
#         doc = docs_service.documents().get(documentId=document_id).execute()
#         doc_content = doc.get("body").get("content")
#         return read_structural_elements(doc_content)


@app.post("/write_cover_letter/")
async def write_cover_letter(payload: Request):
    payload_dict = dict(payload)
    resume = payload_dict["resume"]
    job_description = payload_dict["job_description"]
    name = payload_dict["name"]
    email = payload_dict["email"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1,
        max_tokens=300,
        messages=[{"role": "user", "content": ""}],
    )
    return response.choices[0].message.content
