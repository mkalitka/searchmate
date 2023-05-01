.PHONY: help install clean lint formatter

help:
	@echo "make"
	@echo "    help"
	@echo "        Display this message."
	@echo "    install"
	@echo "        Install or update pic-a-pix."
	@echo "    clean"
	@echo "        Remove Python/build artifacts."
	@echo "    lint"
	@echo "        Lint code with pylint."
	@echo "    formatter"
	@echo "        Format code with black."

install:
	poetry install

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/

lint:
	poetry run pylint searchmate
	poetry run black --check --line-length 80 searchmate

formatter:
	poetry run black --line-length 80 searchmate
