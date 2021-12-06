# Paynica

Dev backend stack:
- fastapi

Dev web stack:
- react

Dev mobile stack:
- react native

## API Server

### Install dependencies

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ cp tmpl.env .env
$ make install
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
