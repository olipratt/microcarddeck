# microcarddeck

A Python 3 REST microservice which exposes an API for playing card decks, used as an example app to explore a REST server which is also a REST client of another server.

Relies on a running [microstore](https://github.com/olipratt/microstore) instance to use to store data.

Once running, go to the root URL to explore the API using [Swagger UI](http://swagger.io/swagger-ui/).

## Setup

Requires at least Python 3, tested with 3.5.

Relies on [Flask](http://flask.pocoo.org/docs/0.11/) and [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/index.html) for the webserver and REST API, and [pyswagger](https://github.com/mission-liao/pyswagger) for the REST client side.

To get these clone the repository, open a terminal inside the repository directory and run:

```shell
$ pip install -r requirements.txt
```

## Running

Run with `-h` for full usage options.

```shell
$ python microcarddeck.py
```

Run the tests by first installing the developer requirements with `pip install -r requirements-dev.txt` then running `python test_microcarddeck.py`.

## Usage

**NOTE:** All API methods are behind a `/api` base URL (Swagger UI hides this away at the very bottom of the web page).

You can explore the API using Swagger UI by opening the root URL (that is printed to the terminal when you run the server) in your web browser.

## Running in Docker

A docker-compose and dockerfile are included to run a multi-microservice-container application. Assuming you've already downloaded and built the microstore image separately, build and run from the repository directory with:

```
$ sudo docker-compose up
```

Now you can navigate to `http://127.0.0.1:5000/` in your web browser to access the SwaggerUI of the card deck app.
