import redis
import json
import time
import random
import logging

# Логування без зайвого шуму
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Підключення до Redis
cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

def simulate_slow_db(key):
    """Імітує повільну операцію отримання даних (наприклад, з бази)"""
    time.sleep(2)
    return {
        "key": key,
        "value": random.randint(1000, 9999),
        "fetched_at": time.strftime("%X")
    }

def get_data_with_cache(key: str, ttl: int = 10):
    """Повертає значення з кешу або повільного джерела"""
    cached = cache.get(key)
    if cached:
        logging.info(f" CACHE HIT: {key}")
        return "HIT", json.loads(cached)
    else:
        logging.info(f" CACHE MISS: {key} — запит до повільного джерела...")
        fresh_data = simulate_slow_db(key)
        cache.setex(key, ttl, json.dumps(fresh_data))
        logging.info(f" CACHE SET: {key} з TTL {ttl} сек")
        return "MISS", fresh_data

# Тестування
if __name__ == "__main__":
    test_key = "user:101"
    for i in range(5):
        print(f"\n Запит №{i+1}")
        t0 = time.time()
        status, data = get_data_with_cache(test_key, ttl=15)
        duration = time.time() - t0
        print(f"{status} | Час: {duration:.2f}s | Дані: {data}")
        print(f"TTL залишилось: {cache.ttl(test_key)} сек\n")
        time.sleep(1)
