.PHONY: help install install-dev install-prod format lint test clean setup-hooks

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install base requirements
	pip install -r requirements/base.txt

install-dev: ## Install development requirements
	pip install -r requirements/dev.txt

install-prod: ## Install production requirements
	pip install -r requirements/prod.txt

setup-hooks: ## Setup pre-commit hooks
	pre-commit install

format: ## Format code with black and isort
	black .
	isort .

lint: ## Run all linters
	flake8 .
	mypy .
	bandit -r . -f json -o bandit-report.json

lint-fix: ## Run formatters and linters with auto-fix
	black .
	isort .
	pyupgrade --py39-plus

test: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage
	pytest

test-watch: ## Run tests in watch mode
	pytest-watch

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

check-all: ## Run all checks (format, lint, test)
	black --check .
	isort --check-only .
	flake8 .
	mypy .
	bandit -r . -f json -o bandit-report.json
	pytest --cov=app --cov-fail-under=80

dev-setup: install-dev setup-hooks ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "Run 'make format' to format code"
	@echo "Run 'make lint' to check code quality"
	@echo "Run 'make test' to run tests"
