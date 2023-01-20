import datetime
import logging
import uuid

from google.cloud import bigquery

from alfred.auth import credentials
from alfred.models import Prompt


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
            prompt.data = ''
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

    def get_latest(self):
        query = f'SELECT * FROM `andresmaro.maro_dataset.alfred` ORDER BY time desc LIMIT 50'
        rows = self.client.query(query).result()
        result = {}
        for row in rows:
            if row.uid in result:
                result[row.uid].append(row)
            else:
                result[row.uid] = [row]
        # _list_ = []
        #
        # for key, value in result.items():
        #     _list_.append(value)

        # result_set = [row.uid for row in rows]
        return result
