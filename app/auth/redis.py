from redis import Redis
from .config import settings

redis_client = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)


def get_redis():
    try:
        redis_client.ping()
        return redis_client
    except Exception:
        raise Exception("Redis connection failed")