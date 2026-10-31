.PHONY: generate reference test lint

generate:
	bash generate.sh

reference:
	python scripts/gen_reference.py

test:
	python -m pytest tests/ -v

lint:
	python -m ruff check .
	python -m ruff format --check .
