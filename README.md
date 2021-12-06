# Paynica

Dev backend stack:
- fastapi

Dev web stack:
- react

Dev mobile stack:
- react native

## API Server

### Install dependencies

- Install dependencies
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements/dev.txt
$ cp tmpl.env .env
```

### Run API server locally

```sh
$ make start
```

### Run tests locally

```sh
$ make test
```

### Run/Fix linters locally

```sh
$ make lint
$ make fix
```