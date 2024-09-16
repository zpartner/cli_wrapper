import json
import os
from pydantic import BaseModel

SECRETS_FILE = 'secrets.json'

class SecretsPayload(BaseModel):
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
    access_token: str
    refresh_token: str
    expires_in: int
    id: int
    tenantUrl: str
    customClient: bool
    token_type: str
    id_token: str
    scope: str
    jti: str
    expires_after: int

def save_secrets(secrets_data: dict):
    """
    Save the provided secrets data to the secrets.json file.
    If the file exists, it will be overwritten. If not, it will be created.
    """
    try:
        with open(SECRETS_FILE, 'w') as f:
            json.dump(secrets_data, f, indent=4)
        return {"message": "Secrets saved successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_secrets():
    """
    Retrieve the secrets from the secrets.json file.
    If the file does not exist, return an empty dictionary.
    """
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}