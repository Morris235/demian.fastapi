from redis.asyncio import Redis

REDIS_URL = "redis://localhost:6379"


async def get_redis() -> Redis:
    redis = Redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()
