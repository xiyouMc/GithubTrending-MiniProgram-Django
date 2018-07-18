import redis
import github_token

class RedisC:
    r = None

    def __init__(self):
        #     pool = redis.ConnectionPool(host='192.168.129.117', port=6379,password = 'video_2017')
        # pool = redis.ConnectionPool(host=ip, port=6379,password=pwd)
        # pool = redis.ConnectionPool(
        #     host='127.0.0.1', port=6379, password=None)
        pool = redis.ConnectionPool(
            host='127.0.0.1', port=6334, password=github_token.redisPass)
        self.r = redis.Redis(connection_pool=pool)

    def _redis_(self):
        return self.r
