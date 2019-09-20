"""Luigi example that mimicks `../dask_distributed/example1.py`"""

import logging

import luigi


logging.basicConfig(level=logging.DEBUG)


class SquareTask(luigi.Task):
    x = luigi.FloatParameter()

    # TODO: Implement output


class NegSquareTask(luigi.Task):
    x = luigi.FloatParameter()

    def requires(self):
        return SquareTask(x=self.x)

    # TODO: Implement output


class SumNegSquareTask(luigi.Task):
    start = luigi.IntParameter()
    stop = luigi.IntParameter()

    def requires(self):
        yield from (NegSquareTask(x) for x in range(self.start, self.stop))

    # TODO: Implement output