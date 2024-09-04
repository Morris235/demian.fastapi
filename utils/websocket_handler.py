import asyncio
import json
import os.path

import requests
import websockets

from api.v1.oauth import get_websocket

WEBSOCKET_FILE: str = 'websocket_cache.json'

# TRADE_MODE가 변경되면 재발급 필요
def response_get_websocket():
    if not os.path.exists(WEBSOCKET_FILE):
        response: requests.Response = get_websocket()
        if response.ok:
            with open(WEBSOCKET_FILE, "w") as f:
                json.dump(response.json(), f)
                f.close()
            print(response.text)
        else:
            print("websocket response error")

def load_websocket_file():
    if os.path.exists(WEBSOCKET_FILE):
        with open(WEBSOCKET_FILE, "r") as f:
            return json.load(f)
    else:
        return {"approval_key": None}



