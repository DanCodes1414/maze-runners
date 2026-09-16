NAME = a_maze_ing.py
CONFIG = config.txt
VENV_FOLDER = .venv
SHELL := /bin/bash

install: check-venv check-pip
	python -m pip install vis_src/ubuntu/mlx-2.2-py3-none-any.whl && \
	python3 -m pip install -U flake8 mypy && \
	python3 -m pip install -r requirements.txt

install-mac: check-venv check-pip
	python -m pip install vis_src/src/mlx_CLXV-2.2.tgz && \
	python3 -m pip install -U flake8 mypy && \
	python3 -m pip install -r requirements.txt

check-venv:
	@command -v python3 >/dev/null || { echo "Error: Python 3 is not installed."; exit 1; }
	@ [ -d "$(VENV_FOLDER)" ] || { echo "Error: Virtual environment not found."; exit 1; }

check-pip:
	@command -v pip >/dev/null || { echo "Error: pip is not installed."; exit 1; }

run:
	python3 $(NAME) $(CONFIG)

debug:
	python3 -m pdb $(NAME) $(CONFIG)

lint:
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --strict

clean:
	rm -rf __pycache__ .mypy_cache
	rm -rf mazegen/__pycache__ mazegen/.mypy_cache
	find . -type f -name "*.txt" -not -name "config.txt" -not -name "requirements.txt" -delete

.PHONY: install run debug lint lint-strict clean check-pip check-venv
