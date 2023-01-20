from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from alfred.ai import AI
from alfred.database import Database
from alfred.speech import Speech
from alfred.models import *

ai = AI()
speech = Speech()
db = Database()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=200)
async def healthcheck():
    return {'healthcheck': 'Everything OK!'}


@app.post("/api/v1/open", status_code=201)
async def open_call(prompt: Prompt):
    response = ai.open_call(prompt)
    return response


@app.post("/api/v1/transcript/cloud", status_code=201)
async def transcript_from_uri(cu: CloudUri):
    response = speech.transcribe_from_uri(cu.gcs_uri)
    return response


@app.get("/api/v1/data/latest", status_code=201)
async def get_latest_prompts():
    response = db.get_latest()
    return response


@app.post("/api/v1/debug", status_code=201)
async def debug_call(prompt: Prompt):
    uid = ai.db.upsert(prompt, "nothing")
    return {"uid": uid}
