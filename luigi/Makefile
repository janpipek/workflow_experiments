.PHONY: default example1 example1-python clean

default:
	@echo "Please, specify the target explicitly."

clean:
	rm -rf example1/

example1:
	luigi --module example1 SumNegSquareTask --local-scheduler --start 0 --stop 10
	@echo
	@echo "Result: "
	@cat example1/sum-0_to_10.txt
	@echo

example1-python:
	python ./example1.py 0 10