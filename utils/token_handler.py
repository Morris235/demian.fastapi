import json
import os.path

from api.v1.oauth import get_token, delete_token
from operations import redis_operations
from operations.redis_operations import redis_client
from utils.time_utils import second_today

TOKEN_FILE = "token_cache.json"

def save_token_cache(token_data):
    redis_operations.set_value(f"token", json.dumps(token_data))
    redis_client.expire("token", 86400)

def load_token_cache() ->  dict[str, int | None]:
    token = redis_operations.get_value("token")
    if token is not None:
        print(token)
        return json.loads(token)
    else:
        return {"access_token": None, "expires_in": 0}

# 시간을 기준으로 24시간 계산하여 토큰 발급
def response_get_token() -> str:
    token_data: dict[str, int | None] = load_token_cache()
    if token_data["access_token"] is None:
        response = get_token()
        save_token_cache(response.json())
        print(response.text)
    return token_data["access_token"]

# redis TTL로 대체
# def response_delete_token():
#     has_token_file = os.path.exists(TOKEN_FILE)
#     if has_token_file:
#         if os.path.getsize(TOKEN_FILE) != 0:
#             token_data: dict[str, int | None] = load_token_cache()
#             if token_data["expires_in"] < second_today():
#                 delete_token(token_data["access_token"])
#                 with open(TOKEN_FILE, "w") as f:
#                     f.truncate(0)
#                     f.close()