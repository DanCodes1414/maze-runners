NAME = a_maze_ing.py

install:
	python3 -m pip install -U flake8 mypy
	python3 -m pip install -r requirements.txt

run:
	python3 $(NAME)

debug:
	python3 -m pdb $(NAME)

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

.PHONY: install run debug clean lint lint-strict