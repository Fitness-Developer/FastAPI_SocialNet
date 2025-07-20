import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()


redis_client = redis.Redis(
    # host=os.getenv("REDIS_HOST", "localhost"),
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True  # auto-decodes utf-8 strings
)

def get_cache(key: str):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key:str, value, expire: int = 60):
    redis_client.setex(key, expire, json.dumps(value))
