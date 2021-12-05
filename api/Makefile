.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1
	rm -rf htmlcov
	rm -rf .coverage


.PHONY: install
install:
	pip install -r requirements/dev.txt
	pre-commit install


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
	TEST_ENV=true pytest --cov=. --cov-report=term --cov-report=html .

