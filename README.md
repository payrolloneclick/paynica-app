# Paynica

Dev backend stack:

- fastapi

Dev frontend stack:

- unknown


## How to run API server locally

- Install dependencies
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements/dev.txt
```

- Run dev server
```sh
$ cp tmpl.env .env
$ make start
```