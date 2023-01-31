# -*- coding: utf-8 -*-

'''
Created on 27-Jan-2023

Author: Priya Kanodia

This file is part of the Radisys Assignment
'''

from micro_fin import app, redis_store


class RedisBase:

    @staticmethod
    def get(key):
        return redis_store.get(key)

    @staticmethod
    def set(key, value, expires=app.config['REDIS_TTL']):
        redis_store.set(key, value)
        if expires is not None:
            redis_store.expire(key, expires)

    @staticmethod
    def remove(key):
        redis_store.delete(key)
    
    @staticmethod
    def set_key_hash(hash_name, key, value):
        return redis_store.hset(hash_name, key, value)

    @staticmethod
    def get_key_hash(hash_name, key):
        return redis_store.hget(hash_name, key)

    @staticmethod
    def delete_key_hash(hash_name, key):
        return redis_store.hdel(hash_name, key)