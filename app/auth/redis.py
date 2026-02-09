import aioredis
from fastapi import Depends


REDIS_URL = "redis://localhost:6379"

async def get_redis():
    redis = await aioredis.from_url(REDIS_URL, decode_responses= True)
    return redis