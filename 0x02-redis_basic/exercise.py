#!/usr/bin/env python3
"""Cache Class"""
from typing import Callable, Union
import uuid
import redis
from functools import wraps

any

def count_calls(method: Callable) -> Callable:
    """
    Count how many times methods of the Cache class are called
    Returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """This is the wrapper"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Input and output history of a method call tracker"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for the decorator."""
        inp = f'{method.__qualname__}:inputs'
        out = f'{method.__qualname__}:outputs'
        fn_out = method(self, *args, **kwargs)
        self._redis.rpush(inp, str(args))
        self._redis.rpush(out, fn_out)
        return fn_out
    return wrapper


def replay(method: Callable) -> None:
    """Prints the replay of a method call."""
    fn_name = method.__qualname__
    inp = f'{fn_name}:inputs'
    out = f'{fn_name}:outputs'
    reds = redis.Redis()
    print('{} was called {} times:'.format(
        fn_name, reds.get(fn_name).decode()))
    for i, o in zip(reds.lrange(inp, 0, -1), reds.lrange(out, 0, -1)):
        print('{}(*{}) -> {}'.format(
            fn_name, i.decode(), o.decode()))


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
    
    def get(self, key: str, fn: [Callable, None] = None) -> None:
        """
        """

        try:
            res: any = self._redis.get(key)
            if res is None:
                return res
            if fn is None:
                return res
            if fn is int:
                res = self.get_int(res)
            elif fn is str:
                res = self.get_str(res)
            else:
                res = fn(res)
            return res
        except Exception as e:
            print(e)

    def get_str(self, res: bytes) -> str:
        """Return the string representation of res(btye)"""
        return str(res)

    def get_int(self, res: bytes) -> int:
        """Return the integer represntation of res(byte)."""
        return int(res)