.PHONY: help lint format test typecheck ci install-hooks clean coverage

help:
	@echo "Commands:"
	@echo "  make lint          # Run ruff linting"
	@echo "  make format        # Run ruff formatting"
	@echo "  make test          # Run pytest tests"
	@echo "  make coverage      # Run tests with coverage report"
	@echo "  make typecheck     # Run mypy type checking"
	@echo "  make ci            # Run all checks (lint, typecheck, test)"
	@echo "  make install-hooks # Install pre-commit hooks"
	@echo "  make clean         # Clean cache and build artifacts"

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

test:
	uv run pytest tests/ -v

coverage:
	uv run pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report: htmlcov/index.html"

typecheck:
	uv run mypy src/

ci: lint typecheck test

install-hooks:
	uv run pre-commit install --hook-type pre-commit --hook-type pre-push

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete