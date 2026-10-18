import os
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = FastAPI()
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.on_event("startup")
async def startup():
    await r.ping()


@app.post("/hit/{key}")
async def hit(key: str):
    count = await r.incr(key)
    return {"key": key, "count": count}


@app.get("/count/{key}")
async def count(key: str):
    count = await r.get(key)
    return {"key": key, "count": int(count or 0)}


@app.get("/healthz")
async def healthz():
    try:
        await r.ping()
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"status": "ok", "redis": "up"}
