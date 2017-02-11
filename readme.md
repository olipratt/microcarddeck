# microcarddeck

A Python 3 REST microservice which exposes an API for playing card decks, used as an example app to explore a REST server which is also a REST client of another server.

Relies on a running [microstore](https://github.com/olipratt/microstore) instance to use to store data.

Once running, go to the root URL to explore the API using [Swagger UI](http://swagger.io/swagger-ui/).

## Setup

Relies on [Flask](http://flask.pocoo.org/docs/0.11/) and [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/index.html) for the webserver and REST API, and [pyswagger](https://github.com/mission-liao/pyswagger) for the REST client side.

Requires [responses](https://github.com/getsentry/responses) for unit testing.

```shell
$ pip install flask flask-restplus pyswagger requests
$ pip install responses
```

Then just clone or download and extract this repository to get started.

## Running

Run with `-h` for full usage options.

```shell
$ python microcarddeck.py
```

Run the tests by similarly running `python test_microcarddeck.py`.

## Usage

**NOTE:** All API methods are behind a `/api` base URL (Swagger UI hides this away at the very bottom of the web page).

You can explore the API using Swagger UI by opening the root URL (that is printed to the terminal when you run the server) in your web browser.
