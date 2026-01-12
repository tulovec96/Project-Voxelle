.PHONY: help install install-dev test test-cov lint format type-check security pre-commit clean build docs run debug

help:
	@echo "Voxelle Development Commands"
	@echo "============================"
	@echo ""
	@echo "Installation:"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo "  make test-fast        - Run tests excluding slow tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run all linters (flake8, pylint)"
	@echo "  make format           - Auto-format code (black, isort)"
	@echo "  make type-check       - Run type checker (mypy)"
	@echo "  make security         - Run security scanner (bandit)"
	@echo "  make pre-commit       - Run all pre-commit checks"
	@echo ""
	@echo "Development:"
	@echo "  make clean            - Remove build artifacts and cache"
	@echo "  make build            - Build distribution packages"
	@echo "  make docs             - Build documentation"
	@echo "  make run              - Run development server"
	@echo "  make debug            - Run with debug logging"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

test-fast:
	pytest -m "not slow"

test-watch:
	pytest-watch

# Linting
lint:
	@echo "Running flake8..."
	flake8 src tests --max-line-length=100 --extend-ignore=E203
	@echo "Running pylint..."
	pylint src --disable=all --enable=E,F

# Formatting
format:
	@echo "Formatting with black..."
	black src tests
	@echo "Sorting imports with isort..."
	isort src tests

# Type checking
type-check:
	mypy src --no-strict-optional

# Security
security:
	bandit -r src --exclude tests/

# Pre-commit
pre-commit:
	pre-commit run --all-files

# Build and documentation
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +

build: clean
	python -m build

docs:
	sphinx-build -W -b html docs/ docs/_build/

# Running
run:
	python src/main.py

debug:
	python -u src/main.py --debug

# Convenient commands
all-checks: format lint type-check security test
	@echo ""
	@echo "✅ All checks passed!"

setup: install-dev pre-commit
	@echo ""
	@echo "✅ Development environment ready!"

# Git hooks
pre-commit-install:
	pre-commit install

pre-commit-uninstall:
	pre-commit uninstall

# Virtual environment
venv:
	python -m venv venv

venv-clean:
	rm -rf venv/

requirements-dev:
	pip freeze > requirements-dev.txt

requirements:
	pip freeze > requirements.txt

.DEFAULT_GOAL := help
