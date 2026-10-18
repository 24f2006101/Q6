import os
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = FastAPI()
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


@app.post("/hit/{key}")
async def hit(key: str):
    try:
        count = await r.incr(key)
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"key": key, "count": count}


@app.get("/count/{key}")
async def count(key: str):
    try:
        count = await r.get(key)
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"key": key, "count": int(count or 0)}


@app.get("/healthz")
async def healthz():
    try:
        await r.ping()
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"status": "ok", "redis": "up"}
