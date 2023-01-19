import os

from dotenv import load_dotenv
from google.oauth2 import service_account

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


def get_credentials():
    return credentials
