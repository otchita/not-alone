.PHONY: clean clean-test clean-docs clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

ifeq (, $(shell which snakeviz))
	PROFILE = pytest --profile-svg
	PROFILE_RESULT = prof/combined.svg
	PROFILE_VIEWER = $(BROWSER)
else
    PROFILE = pytest --profile
    PROFILE_RESULT = prof/combined.prof
	PROFILE_VIEWER = snakeviz
endif

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -path ./.venv -prune -false -name '*.egg-info' -exec rm -fr {} +
	find . -path ./.venv -prune -false -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -path ./.venv -prune -false -name '*.pyc' -exec rm -f {} +
	find . -path ./.venv -prune -false -name '*.pyo' -exec rm -f {} +
	find . -path ./.venv -prune -false -name '*~' -exec rm -f {} +
	find . -path ./.venv -prune -false -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	rm -fr prof/

clean-docs: ## remove docs artifacts
	rm -fr docs/_build
	rm -fr docs/api

lint: ## check style with flake8
	flake8 nalone tests
	pylint nalone tests

test: ## run tests quickly with the default Python
	pytest

test-typing: ## check static typing using mypy
	mypy nalone

test-docs: docs-api ## check docs using doc8
	pydocstyle nalone
	doc8 docs *.rst --ignore-path docs/_build
	$(MAKE) -C docs doctest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source nalone -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

profile:  ## create a profile from test cases
	$(PROFILE) $(TARGET)
	$(PROFILE_VIEWER) $(PROFILE_RESULT)

docs-api:  ## generate the API documentation for Sphinx
	rm -rf docs/api
	sphinx-apidoc -e -M -o docs/api nalone

docs: docs-api ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
