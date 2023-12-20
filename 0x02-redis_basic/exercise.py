#!/usr/bin/env python3
"""ALX SE Backend Redis Module."""
import redis
from typing import Union, Callable, Any
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
      Keep track of the amount of times a method with
      access to a redis instance is call.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """This is the wrapper itself."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Keep history of the input and output of a method call."""
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
    """Print the replay of a method call."""
    fn_name = method.__qualname__
    inp = f'{fn_name}:inputs'
    out = f'{fn_name}:outputs'
    reds = redis.Redis()
    print('{} was called {} times:'.format(
        fn_name, reds.get(fn_name).decode()))
    for i, o in zip(reds.lrange(inp, 0, -1), reds.lrange(out, 0, -1)):
        print('{}(*{}) -> {}'.format(
            fn_name, i.decode(), o.decode()))


class Cache:
    """This model implement a simple caching machanism using redis."""
    def __init__(self) -> None:
        """Initialize my cache model."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
          Store the data with a random key generated
          from uuid4 and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn: Union[Callable, None] = None):
        """Return the res of a key in its rightful type."""
        res: Any = self._redis.get(key)

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

    def get_str(self, res: bytes) -> str:
        """Return the string representation of res"""
        return str(res)

    def get_int(self, res: bytes) -> int:
        """Return the integer representation of res"""
        return int(res)