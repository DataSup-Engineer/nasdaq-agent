# NASDAQ Stock Agent - Development Makefile

.PHONY: help install dev run test clean lint format

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  dev        - Install development dependencies"
	@echo "  run        - Run the application"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code"
	@echo "  clean      - Clean build artifacts"

install:
	pip install -r requirements.txt

dev: install
	pip install -e .

run:
	python main.py

test:
	pytest

lint:
	flake8 src/
	flake8 main.py

format:
	black src/
	black main.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete