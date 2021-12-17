.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1
	rm -rf htmlcov
	rm -rf .coverage


.PHONY: start
start:
	uvicorn main:app --reload --port=8080


.PHONY: fix
fix:
	black .
	isort .


.PHONY: lint
lint:
	flake8 --show-source .
	interrogate --config setup.cfg .
	isort --check-only . --diff


.PHONY: test
test:
	ENV_FILE=tmpl.env pytest --cov=. --cov-report=term --cov-report=html .
