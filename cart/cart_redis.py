import logging
import json
from book.redis_service import RedisService, RedisKey


class RedisCart(RedisKey):
    def __init__(self):
        self.redis = RedisService()
        self.key = "cart"

    def get_cart(self, key):
        """get book from memory"""
        try:
            cart = self.redis.getter(str(key))
            if cart is not None:
                return json.loads(cart)
            return {}
        except Exception as err:
            logging.error(err)

    def add_cart(self, key, cart):
        """adding book to memory"""
        try:
            self.gen_key = self.key
            id = self.key_generator(key)
            cart_dict = self.get_cart(id)
            cart_dict.update({cart.get('id'): cart})
            self.redis.setter(str(id), json.dumps(cart_dict))
        except Exception as err:
            logging.error(err)

    def delete_cart(self, key, cart):
        """deleting the book from the memory"""
        try:
            self.gen_key = self.key
            id = self.key_generator(key)
            cart_dict = self.get_cart(id)
            cart_dict.pop(str(id))
            self.redis.setter(str(id), json.dumps(cart_dict))

        except Exception as err:
            logging.exception(err)
