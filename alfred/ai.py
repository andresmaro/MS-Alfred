import os

import openai
from dotenv import load_dotenv

from alfred.database import Database
from alfred.models import Prompt

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class AI:
    def __init__(self):
        self.db = Database()

    def open_call(self, prompt: Prompt):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{prompt.instruction}: {prompt.data}",
            temperature=0.7,
            max_tokens=250,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        response.uid = self.db.upsert(prompt, response.choices[0].text)
        return response
