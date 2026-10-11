.PHONY: install test lint format build clean publish-test check

install:
	pip install -e ".[dev,crosscheck]"

test:
	pytest --cov --cov-report=term-missing

lint:
	ruff check .
	ruff format --check .

format:
	ruff check --fix .
	ruff format .

build:
	python -m build

check: lint test build
	@echo "all green"

publish-test:
	python -m build
	twine check dist/*
	twine upload --repository testpypi dist/*

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache htmlcov .coverage
	find . -name __pycache__ -type d -exec rm -rf {} +
