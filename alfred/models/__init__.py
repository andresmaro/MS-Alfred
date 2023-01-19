from pydantic import BaseModel


class Prompt(BaseModel):
    uid: str = None
    instruction: str
    data: str
