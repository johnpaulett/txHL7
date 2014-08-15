VIRTUALENV = env
PYTHON = $(VIRTUALENV)/bin/python
PIP = $(VIRTUALENV)/bin/pip
TRIAL = $(VIRTUALENV)/bin/trial
FLAKE8 = $(VIRTUALENV)/bin/flake8

.PHONY: lint tests

env: requirements.txt
	test -f $(PYTHON) || virtualenv --no-site-packages env
	$(PIP) install -r requirements.txt

lint: env
	$(FLAKE8) --ignore=F821 twistedhl7
	# E501 -- hl7 sample messages can be long, ignore long lines in tests
	$(FLAKE8) --ignore=E501 tests

tests: env
	$(TRIAL) tests
