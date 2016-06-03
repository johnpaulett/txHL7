.PHONY: tests build docs lint upload

BIN = env/bin
PYTHON = $(BIN)/python
PIP = $(BIN)/pip
TRIAL = $(BIN)/trial
TOX = $(BIN)/tox

SPHINXBUILD   = $(shell pwd)/env/bin/sphinx-build

env: requirements.txt
	test -f $(PYTHON) || virtualenv --no-site-packages env
	$(PIP) install -U -r requirements.txt
	$(PYTHON) setup.py develop

tests: env
	$(TOX)

build:
	$(PYTHON) setup.py sdist

clean-docs:
	cd docs; make clean

docs: env
	cd docs; make html SPHINXBUILD=$(SPHINXBUILD); make man SPHINXBUILD=$(SPHINXBUILD); make doctest SPHINXBUILD=$(SPHINXBUILD)

lint: env
	$(BIN)/flake8 txHL7 tests twisted
	$(BIN)/isort --recursive --check-only txHL7 tests twisted

isort:
	$(BIN)/isort --recursive txHL7 tests twisted

upload: build
	$(PYTHON) setup.py sdist register upload

clean:
	find txHL7 twisted tests -type f -name '*.pyc' -delete
