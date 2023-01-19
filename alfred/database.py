import datetime
import json
import logging
import os
import uuid
import json

from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account

from alfred.models import Prompt

load_dotenv()

credentials = service_account.Credentials.from_service_account_info(
    {
        "type": os.getenv("GCP_TYPE"),
        "project_id": os.getenv("GCP_PROJECT_ID"),
        "private_key_id": os.getenv("GCP_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GCP_PRIVATE_KEY"),
        "client_email": os.getenv("GCP_CLIENT_EMAIL"),
        "client_id": os.getenv("GCP_CLIENT_I"),
        "auth_uri": os.getenv("GCP_AUTH_URI"),
        "token_uri": os.getenv("GCP_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GCP_AUTH_PROVIDER_CERT"),
        "client_x509_cert_url": os.getenv("GCP_CLIENT_CERT"),
    }
)


class Database:
    def __init__(self):
        self.client = bigquery.Client(credentials=credentials)
        self.table = self.client.get_table("maro_dataset.alfred")

    def upsert(self, prompt: Prompt, answer):
        if prompt.uid is None:
            uid = uuid.uuid4().hex
            self.insert_items(prompt, answer, uid)
            return uid
        else:
            prompt.data=''
            self.insert_items(prompt, answer, prompt.uid)
            return prompt.uid

    def insert_items(self, prompt: Prompt, answer, uid):
        errors = self.client.insert_rows(self.table, [
            {
                "uid": uid,
                "data": prompt.data,
                "type": "open",
                "prompt": prompt.instruction,
                "answer": answer,
                "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            }])
        if not errors:
            logging.info("save success")
            print("save success")
        else:
            logging.error("Encountered errors while inserting rows: {}".format(errors))

    def get_latest(self, source):
        query = f'SELECT * FROM `andresmaro.maro_dataset.cripto_alerts` WHERE `source` = "{source}" ORDER BY time desc LIMIT 100'
        rows = self.client.query(query).result()
        result_set = [row.hash for row in rows]
        return result_set
