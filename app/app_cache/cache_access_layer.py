import json
from app.app_cache import redis_cache

# ASSUMPTION : static data : if a key has value it does not change over time

from app.app_cache.async_cache_update import AsyncCacheUpdate
from app.utils import logger


def get_bank(key: str):
    result = redis_cache.get(key.lower())
    if result:
        return json.loads(result)
    return None


def set_bank(key: str, bank_details: dict):

    # if value is present previously then skip adding
    if get_bank(key=key):
        return True

    result = redis_cache.set(key.lower(), json.dumps(bank_details))
    if result:
        return True
    return False


def get_branch_details(bank_name: str, city: str):
    result = redis_cache.hget(city.lower(), bank_name.lower())
    if result:
        return json.loads(result)
    return None


def set_branch_details(bank_name: str, city: str, branches_list: list):

    # if value is present previously then skip adding
    if get_branch_details(bank_name, city):
        return True

    result = redis_cache.hset(city.lower(), bank_name.lower(), json.dumps(branches_list))
    if result:
        return True
    return False


def cache_update(func, *args):
    thread = AsyncCacheUpdate(func, args)
    thread.start()


def redis_keys():
    return redis_cache.keys()