import redis

def connectredis():
    # Connect to Redis
    redis_host = 'redis-17072.c285.us-west-2-2.ec2.cloud.redislabs.com'
    redis_port = 17072
    pw = '4PLTzbkfHThICHNiBqoL2PGnljfBK8bh'
    redis_client = redis.Redis(host=redis_host, port=redis_port, password=pw)
    return redis_client

