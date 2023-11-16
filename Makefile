SHELL := /bin/bash
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

clean: ## cleans python for wheel
	find src -type f -name '*.pyc' -delete 2>/dev/null
	find src -type d -name '__pycache__' -delete 2>/dev/null
	rm -rf build dist **/*.egg-info .pytest_cache rust-query-crlite/target
	rm -f **/*.zip **/*.tgz **/*.gz .coverage

deps: ## install dependancies for development of this project
	pip install --disable-pip-version-check -U pip
	pip install -e .

install-dev: ## Install the package
	pip install --disable-pip-version-check -U pip
	pip install -U build twine setuptools pytest wheel coverage
	pip install --force-reinstall --no-cache-dir -e .

test: ## run unit tests with coverage
	coverage run -m pytest --nf
	coverage report -m

build: ## build wheel file
	rm -f dist/*
	python -m build -nxsw

publish: ## upload to pypi.org
	python -m twine upload dist/*
