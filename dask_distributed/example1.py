import logging

from dask.distributed import Client

logging.basicConfig(level=logging.DEBUG)


def square(x):
        return x ** 2

def neg(x):
        return -x


if __name__ == "__main__":
    # This automatically creates the server and also workers
    client = Client()

    A = client.map(square, range(10))
    B = client.map(neg, A)
    total = client.submit(sum, B)
    print(total.result())