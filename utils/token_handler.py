import json
import os.path

from api.v1.oauth import get_token, delete_token
from utils.time_utils import second_today

TOKEN_FILE = "token_cache.json"

def save_token_to_file(token_data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
        f.close()

def load_token_from_file() ->  dict[str, int | None]:
    has_token_file = os.path.exists(TOKEN_FILE)
    if has_token_file:
        if os.path.getsize(TOKEN_FILE) != 0:
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
    return {"access_token": None, "expires_in": 0}

def response_get_token() -> str:
    token_data: dict[str, int | None] = load_token_from_file()
    if token_data["access_token"] is None or token_data["expires_in"] < second_today():
        response = get_token()
        save_token_to_file(response.json())
        print(response.text)
    return token_data["access_token"]

def response_delete_token():
    has_token_file = os.path.exists(TOKEN_FILE)
    if has_token_file:
        if os.path.getsize(TOKEN_FILE) != 0:
            token_data: dict[str, int | None] = load_token_from_file()
            if token_data["expires_in"] < second_today():
                delete_token(token_data["access_token"])
                with open(TOKEN_FILE, "w") as f:
                    f.truncate(0)
                    f.close()