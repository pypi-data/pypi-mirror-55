from functools import wraps
from time import time, sleep


class DynamicWait:
    """ sleep dynamically by measuring the time passed
    since t started and sleeping the
    remaining of the delay
    """

    def __init__(self, duration=None):
        self.t = time()
        self.d = duration

    def __call__(self, duration=None):
        if duration is None:
            if self.d is None:
                raise ValueError(
                    "missing duration parameter")
            duration = self.d
        t = time() - self.t
        if t < duration:
            sleep(duration - t)


class timer:
    """
    a while timer

    usage example:
        running = timer(2)
        while running:
            print("loop for 2 seconds")
    """
    def __init__(self, duration):
        self.duration = duration
        self.timestamp = time()

    def __bool__(self):
        return time() - self.timestamp < self.duration


def task_duration(delay):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            wait = DynamicWait(delay)
            results = function(*args, **kwargs)
            wait()
            return results
        return wrapper
    return decorator
