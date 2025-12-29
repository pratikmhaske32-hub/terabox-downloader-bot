# redis_db.py
import os
import redis
import threading
import time

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

db = None
REDIS_AVAILABLE = False


def connect_redis():
    global db, REDIS_AVAILABLE
    try:
        db = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
        )
        db.ping()
        REDIS_AVAILABLE = True
        print("✅ Redis connected")
    except Exception as e:
        REDIS_AVAILABLE = False
        db = None
        print("⚠️ Redis not available, continuing without cache:", e)


connect_redis()


def re_cache():
    while True:
        try:
            if REDIS_AVAILABLE and db:
                db.keys("*")
        except Exception as e:
            print("⚠️ Redis re_cache error:", e)
        time.sleep(30)


threading.Thread(target=re_cache, daemon=True).start()
