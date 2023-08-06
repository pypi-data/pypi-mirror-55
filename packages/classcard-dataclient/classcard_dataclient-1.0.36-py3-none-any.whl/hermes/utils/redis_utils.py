import redis
import json
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD


class RedisQueue(object):
    def __init__(self, name, namespace='HERMES_QUEUE', **redis_kwargs):
        default_kwargs = {"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB, "password": REDIS_PASSWORD}
        default_kwargs.update(redis_kwargs)
        self.__pool = redis.ConnectionPool(**default_kwargs)
        self.__db = redis.Redis(self.__pool)
        self.key = '{}:{}'.format(namespace, name)

    def reconnect(self):
        self.__db.ping()

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        if isinstance(item, dict):
            item = json.dumps(item)
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None, loads=True):
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        if item:
            item = item[1].decode("utf-8")
            if loads:
                item = json.loads(item)
        return item
