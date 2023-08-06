from time import time
import functools


def timing(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('{} :Elapsed time: {}'.format(f.__name__, end-start))
        return result
    return wrapper
