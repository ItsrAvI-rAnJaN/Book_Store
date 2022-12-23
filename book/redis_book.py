import logging
import json
from book.redis_service import RedisService, RedisKey


class RedisBook(RedisKey):

    def __init__(self):
        self.redis = RedisService()
        self.key="book"

    def get_book(self, key):
        """get book from memory"""
        try:
            books = self.redis.getter(str(key))
            if books is not None:
                return json.loads(books)
            return {}

        except Exception as e:
            logging.error(e)

    def add_book(self, key, book):
        """adding book to memory"""
        try:
            self.gen_key=self.key
            id=self.key_generator(key)
            book_dict = self.get_book(id)
            book_dict.update({book.get('id'): book})
            self.redis.setter(str(id), json.dumps(book_dict))
        except Exception as e:
            logging.error(e)

    def update_book(self, key, book):
        """delete book from memory"""
        self.gen_key = self.key
        id = self.key_generator(key)
        book_id = str(book.get('id'))
        books_dict = self.get_book(key)
        book = books_dict.get(id)
        if book is not None:
            books_dict.update({id: book})
            self.redis.setter(key, json.dumps(books_dict))

    def delete_note(self, key, id):
        """deleting the book from the memory"""
        try:
            self.gen_key = self.key
            id = self.key_generator(key)
            book_dict = self.get_book(id)
            book_dict.pop(str(id))
            self.redis.setter(str(id), json.dumps(book_dict))

        except Exception as error:
            logging.exception(error)
