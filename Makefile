VIRTUALENV = env
PYTHON = $(VIRTUALENV)/bin/python
PIP = $(VIRTUALENV)/bin/pip
TRIAL = $(VIRTUALENV)/bin/trial

.PHONY: tests

env: requirements.txt
	test -f $(PYTHON) || virtualenv --no-site-packages env
	$(PIP) install -r requirements.txt

tests: env
	$(TRIAL) tests
