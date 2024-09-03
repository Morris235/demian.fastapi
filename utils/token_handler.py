import json
import os.path

from api.v1.oauth import get_token, delete_token
from utils.time_utils import second_today

TOKEN_FILE = "token_cache.json"

def save_token_to_file(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def load_token_from_file():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {"access_token": None, "expires_in": 0}

async def response_get_token():
    token_data = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        response = get_token()
        save_token_to_file(response.json())
        print(response.text)
    return token_data["access_token"]

async def response_delete_token():
    token_data = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        return {"response" : "already deleted"}
    os.remove(TOKEN_FILE)
    response = delete_token(token_data["access_token"])
    return response