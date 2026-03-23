from pyexpat.errors import messages
from redis.asyncio import Redis

REDIS_URL = "redis://127.0.0.1:6379"

# Initialize as None initially
redis_client: Redis | None = None

async def init_redis():
    global redis_client
    redis_client = Redis.from_url(
        REDIS_URL,
        decode_responses=True
    )

def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized. Ensure init_redis() is called in lifespan.")
    return redis_client