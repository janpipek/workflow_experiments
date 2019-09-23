import logging
import os
import multiprocessing
import time

"""Simple example showing the inner workings of celery."""
from celery import Celery
from celery.exceptions import TimeoutError


REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

logging.basicConfig(level=logging.DEBUG)


# Main application object shared between server and client
app = Celery("example1", broker=f"redis://:{REDIS_PASSWORD}@localhost/0", backend=f"redis://:{REDIS_PASSWORD}@localhost")


@app.task
def add(x, y):
    time.sleep(2)
    return x + y


if __name__ == "__main__":
    # Fork a new process with the server
    logging.debug("Starting the server.")
    worker_process = multiprocessing.Process(target=app.worker_main)
    worker_process.start()

    try:
        # This is the client branch
        logging.debug("Starting the client.")

        # Submit the task (asynchronously).
        result = add.delay(4, 4)
        logging.debug("Submitted the calculation of 4+4".)
        try:
            result.get(timeout=0.1)
        except TimeoutError:
            logging.debug("Result not yet ready (0.1 s timeout)")

        logging.debug("Waiting for the result indefinitely.")
        value = result.get()

        logging.debug(f"Result {value} obtained.")

    finally:
        # It is necessary to kill the worker, otherwise it runs indefinitely
        worker_process.kill()


    