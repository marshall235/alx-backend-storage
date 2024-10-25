#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method,
store an instance of the Redis client as a
private variable named _redis (using redis.
Redis()) and flush the instance using flushdb.

Create a store method that takes a data argument
and returns a string. The method should generate
a random key (e.g. using uuid), store the input
data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data
can be a str, bytes, int or float.
"""


import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method:  Callable) -> Callable:
    """ Returns a Callable """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Store the history of inputs and outputs
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """Displays the history calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

        print(f"{function_name} was called {value} times")
        inputs = r.lrange(f"{function_name}:inputs", 0, -1)

        ouputs = r.lrange(f"{function_name}:outputs", 0, -1)

        for input, output in zip(inputs, outputs):
            try:
                input = input.decode("utf-8")
            except Exception:
                input = ""

            try:
                output = output.decode("utf-8")
            except Exception:
                output = ""

                print(f"{function_name}(*{input}) -> {output}")


class Cache:
    """Create class cache"""

    def __init__(self):
        """
        Stores the Redis client instance
        and flushes Redis Database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generate a random key """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Convert the data back to the desired format"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Automatically parametize Cache.get with correct
        conversion function"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: int) -> Optional[int]:
        """ Automatically parametize Cache,get with correct
        conversion function"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
