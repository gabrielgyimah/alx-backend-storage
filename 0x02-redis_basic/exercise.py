#!/usr/bin/env python3
"""Cache Class"""
from typing import Union
import uuid
import redis


class Cache():
    """Cache class"""

    def __init__(self) -> None:
        """Initializes an instance of the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """"
        generates a random key (e.g. using uuid)
        store the input data in Redis using the random key
        returns key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key