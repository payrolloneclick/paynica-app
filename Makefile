
.PHONY: install
install:
	pip install -r ./api/requirements/dev.txt
	yarn --cwd ./app install
	pre-commit install
