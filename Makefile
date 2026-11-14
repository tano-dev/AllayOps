.PHONY: help test lint format typecheck repo-map benchmark server

PYTHON ?= python

help:
	@echo "AllayOps Enterprise Task Runner"
	@echo "  make test       - Run all unit & contract tests"
	@echo "  make lint       - Run Ruff linter"
	@echo "  make format     - Check Ruff formatting"
	@echo "  make typecheck  - Run Mypy static type checker"
	@echo "  make repo-map   - Regenerate docs/architecture/repo_map.json"
	@echo "  make benchmark  - Run canonical Minecraft chaos benchmark"

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format --check .

typecheck:
	$(PYTHON) -m mypy shared_interfaces minecraft_plane observability_plane agentic_plane research

repo-map:
	$(PYTHON) scripts/generate_repo_map.py

codegraph:
	$(PYTHON) scripts/generate_codegraph.py

benchmark:
	$(PYTHON) -m research.run_benchmark

server:
	cmd /c start.bat
