from app.utils.config_access import config
import redis


redis_cache = redis.Redis(host=config['REDIS_HOST'], port=config['REDIS_PORT'], db=config['REDIS_DB'])