.PHONY: help lint format test typecheck ci install-hooks

help:
	@echo "Commands:"
	@echo "  make lint        # Run ruff linting"
	@echo "  make format      # Run ruff formatting"
	@echo "  make test        # Run pytest tests"
	@echo "  make typecheck   # Run mypy type checking"
	@echo "  make ci          # Run all checks (lint, typecheck, test)"
	@echo "  make install-hooks  # Install pre-commit hooks"

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

test:
	uv run pytest tests/ -v

typecheck:
	uv run mypy src/

ci: lint typecheck test

install-hooks:
	uv run pre-commit install