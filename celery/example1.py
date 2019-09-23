"""Simple example computing a sum of negative squares for the range (0, 10)."""
import logging
import os
import multiprocessing
import time

from celery import Celery, chain, chord


REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

logging.basicConfig(level=logging.DEBUG)


# Main application object shared between server and client
app = Celery("example1", broker=f"redis://:{REDIS_PASSWORD}@localhost/0", backend=f"redis://:{REDIS_PASSWORD}@localhost")


@app.task()
def square(x):
    return x ** 2


@app.task()
def neg(x):
    return -x


@app.task()
def sum_(xs):
    return sum(xs)


if __name__ == "__main__":
    worker_process = multiprocessing.Process(target=app.worker_main)
    worker_process.start()

    try:
        result = chord(
            (square.s(i) | neg.s() for i in range(10)),
            sum_.s()
        )()
        value = result.get()

        logging.debug(f"Result {value} obtained.")

    finally:
        worker_process.kill()