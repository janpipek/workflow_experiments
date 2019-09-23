"""Simple example computing a sum of negative squares for the range (0, 10).

You can run this example:
- as a standalone script:

    python example1.py 0 10

- as a luigi task started by luigi itself:

    luigi --module example1 SumNegSquareTask --local-scheduler --start 0 --stop 10

Note: Unfortunately, the intermediate results are written to local files.
"""

import logging
import os
import sys

import luigi

basedir = os.path.join(os.path.dirname(__file__), "example1")


logging.basicConfig(level=logging.DEBUG)


class SquareTask(luigi.Task):
    x = luigi.IntParameter()

    def output(self):
        return luigi.LocalTarget(os.path.join(basedir, f"{self.x}-square.txt"))

    def run(self):
        with self.output().open("w") as outfile:
            outfile.write(str(self.x ** 2))


class NegSquareTask(luigi.Task):
    x = luigi.IntParameter()

    def requires(self):
        return SquareTask(x=self.x)

    def run(self):
        with self.input().open("r") as infile:
            squared = int(infile.read().strip())

        with self.output().open("w") as outfile:
            outfile.write(str(-squared))

    def output(self):
        return luigi.LocalTarget(os.path.join(basedir, f"{self.x}-neg_square.txt"))


class SumNegSquareTask(luigi.Task):
    start = luigi.IntParameter()
    stop = luigi.IntParameter()

    def requires(self):
        yield from (NegSquareTask(x) for x in range(self.start, self.stop))

    def run(self):
        result = 0
        for input in self.input():
            with input.open("r") as infile:
                result += int(infile.read().strip())

        with self.output().open("w") as outfile:
            outfile.write(str(result))

    def output(self):
        return luigi.LocalTarget(os.path.join(basedir, f"sum-{self.start}_to_{self.stop}.txt"))


if __name__ == "__main__":
    start, stop = (int(arg) for arg in sys.argv[1:3])
    task = SumNegSquareTask(start=start, stop=stop)
    result = luigi.build([task], local_scheduler=True)
    
    with task.output().open() as infile:
        result = int(infile.read().strip())

    print(f"Result: {result}")