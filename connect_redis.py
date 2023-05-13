import redis

def connect():
    # Connect to Redis
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    return redis_client