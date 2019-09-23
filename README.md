# workflow_experiments

My personal experiments with various workflow managements / scheduler systems in Python:

- celery
- dask distributed
- luigi
- airflow (not yet started)
- spark (not yet started)

## Installation

1) Install local redis. Follow <https://redis.io/>.

2) Optionally create a virtual environment.

3) Install requirements.

```
pip install -e requirements.txt
```

4) Optionally set up environment variables 

- `REDIS_PASSWORD`: password to the local redis instance

## Examples

Examples with the same name in each directory show a solution to the same problem.

- example1.py

```
sum(-x ** 2 for x in range(10))
```

## Usage

Follow the Makefiles.

## Note

Some of the copies are trivally copied from tutorials, manuals.
