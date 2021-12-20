# Paynica

Dev backend stack (api folder):

- fastapi

Dev web stack (app folder):

- react
- typescript

Dev mobile stack:

- react native

## Install environment

```sh
$ pyenv local 3.10.0
$ python --version
$ python -m venv api/.venv
$ source api/.venv/bin/activate
(.venv) $ make install
```

## API Server

### Run locally

```sh
$ cd api
$ make start
```

### Run tests locally

```sh
$ cd api
$ make test
```

### Run/Fix linters locally

```sh
$ cd api
$ make lint
$ make fix
```

## APP Client

### Run locally

```sh
$ cd app
$ make start
```

### Run tests locally

```sh
$ cd app
$ make test
```

### Run/Fix linters locally

```sh
$ cd app
$ make lint
$ make fix
```
