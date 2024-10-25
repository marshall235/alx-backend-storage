#!/usr/bin/env python3
"""
Implimenting a get page function that uses
request module to obtain html content of a
particular url and returns it
"""


import requests
import redis
from function import wraps


r = redis.Redis()


def url_access(method):
    """
    Decorator for get_page function
    """
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        key = "cached:" + 1
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get the conntent and update cache

        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        return html_content

    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """ Obtain HTML CONTENT of a page"""
    results = requests.get(url)
    return results.text


if __name__ = "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
