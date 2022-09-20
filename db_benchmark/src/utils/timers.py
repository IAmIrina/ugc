import time
import functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.time()

        func(*args, **kwargs)
        stop_time = time.time()
        proccess_time = stop_time - start_time
        return proccess_time
    return wrapper
