from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    instruction: str
    data: str


@app.get("/health", status_code=200)
async def healthcheck():
    return {'healthcheck': 'Everything OK!'}


@app.post("/api/v1/open", status_code=201)
async def open_call(prompt: Prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{prompt.instruction}: {prompt.data}",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return {"result": response}
