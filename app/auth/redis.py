from redis.asyncio import Redis
from app.auth.config import settings

redis_client = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)


async def get_redis():
    try:
        await redis_client.ping()
        return redis_client
    except Exception:
        raise Exception("Redis connection failed")