from core.redis_config import redis_config

redis_client = redis_config()

def set_value(key: str, value: str) -> bool:
    if redis_client is None:
        raise Exception("Redis connection failure")

    try:
        redis_client.set(key, value)
        return True
    except Exception as e:
        print(f"Error setting value: {e}")
        return False


def get_value(key: str) -> str | None:
    if redis_client is None:
        raise Exception("Redis connection failure")

    try:
        value = redis_client.get(key)
        if value:
            return value.decode("utf-8")
        else:
            return None
    except Exception as e:
        print(f"Error getting value: {e}")
        return None


def delete_value(key: str) -> bool:
    if redis_client is None:
        raise Exception("Redis connection failure")

    try:
        result = redis_client.delete(key)
        return result > 0  # Redis의 delete 명령은 삭제된 키의 수를 반환
    except Exception as e:
        print(f"Error deleting value: {e}")
        return False