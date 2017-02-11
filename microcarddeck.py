'''
A simple REST playing card deck API.

Once running, go to the root URL to explore the API using
[swaggerui](http://swagger.io/swagger-ui/).
'''
import logging
import sys
import argparse

import deckstore
from deckserver import app


log = logging.getLogger(__name__)


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='REST Playing Card Deck')
    parser.add_argument('datastore_schema', metavar='SCHEMA-URL', type=str,
                        help='URL of Swagger schema for the datastore to use')
    parser.add_argument('--host', metavar='IP', type=str,
                        default=None,
                        help="hostname to listen on - set this to '0.0.0.0' "
                             "to have the server available externally as "
                             "well. Defaults to '127.0.0.1'")
    parser.add_argument('--port', metavar='PORT', type=int,
                        default=None,
                        help='the port of the webserver - defaults to 5000')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='turn on debug logging')

    parsed_args = parser.parse_args(raw_args)
    return parsed_args


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    logging.basicConfig(format='%(asctime)-15s:%(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.getLogger("pyswagger").setLevel(logging.WARNING)

    deckstore.init(args.datastore_schema)
    app.run(host=args.host, port=args.port)
    deckstore.term()
