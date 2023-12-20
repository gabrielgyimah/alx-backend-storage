#!/usr/bin/env python3
"""Web Caching Module."""
import requests
import redis
from typing import Callable
from functools import wraps


cache = redis.Redis()


def store_cache(method: Callable) -> Callable:
    """Cache an item with 10 seconds ttl"""
    @wraps(method)
    def wrapper(url):
        """The function wrapper."""
        if cache.get(url):
            return cache.get(url).decode()
        content = method(url)
        cache.setex(url, 10, content)
        return content
    return wrapper


def track_url(method: Callable) -> Callable:
    """Cache an item with 10 sec ttl"""
    @wraps(method)
    def wrapper(url):
        """The function wrapper."""
        cache.incr(f'count:{url}')
        return method(url)
    return wrapper


@store_cache
@track_url
def get_page(url: str) -> str:
    """Get the content of a webpage"""
    if cache.get(url):
        return cache.get(url).decode()
    content = requests.get(url)
    return content.text