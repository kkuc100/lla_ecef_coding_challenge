.PHONY: test run

PYTHON=python3
MAIN_SCRIPT=ecef_solution.py
TEST_SCRIPT=ecef_code_unittest.py

test:
	$(PYTHON) $(TEST_SCRIPT)

run:
	$(PYTHON) $(MAIN_SCRIPT)
