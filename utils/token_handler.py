import json
from api.v1.oauth import get_token
from core.redis_config import redis_config

rd = redis_config()

def save_token_cache(token_data):
    rd.set(f"token", json.dumps(token_data), ex=86400)

def load_token_cache() ->  dict[str, int | None]:
    token = rd.get("token")
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