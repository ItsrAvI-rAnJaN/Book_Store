import redis
import logging

redis_connection = redis.Redis(host='localhost', port=6379)
logging.basicConfig(filename='user_logs.log', encoding='utf-8', level=logging.DEBUG)


class RedisService:

    def getter(self, key):
        try:
            return redis_connection.get(key)
        except redis.exceptions.RedisError as err:
            logging.exception(err)

    def setter(self, key, value):
        try:
            return redis_connection.set(key, value)
        except redis.exceptions.RedisError as err:
            logging.exception(err)


class RedisKey:
    gen_key = None

    def key_generator(self, id):
        if self.gen_key is not None:
            return f"{self.gen_key}_{id}"
