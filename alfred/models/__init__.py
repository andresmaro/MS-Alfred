from pydantic import BaseModel


class Prompt(BaseModel):
    uid: str = None
    instruction: str
    data: str


class CloudUri(BaseModel):
    gcs_uri: str
