"""Simple example computing a sum of negative squares for the range (0, 10).

Joblib can parallelize function calls but does not provide any workflow mechanism.
"""
from joblib import Parallel, delayed


def square(x):
        return x ** 2


def neg(x):
        return -x


def chain(x):
    return neg(square(x))


if __name__ == "__main__":
    parallel = Parallel(verbose=51, prefer="processes", n_jobs=5)
    intermediate = parallel(delayed(chain)(x) for x in range(10))
    result = sum(intermediate)
    print(f"Result: {result}")
    