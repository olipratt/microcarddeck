'''
A simple REST playing card deck API.

Once running, go to the root URL to explore the API using
[swaggerui](http://swagger.io/swagger-ui/).
'''
import logging
import sys
import argparse

from flask import Flask
from flask_restplus import Resource, Api, fields


log = logging.getLogger(__name__)
app = Flask(__name__)

# Use a non-empty 'prefix' (becomes swagger 'basePath') for interop reasons -
# if it's empty then the basePath is '/', which with an API enpoint appended
# becomes '//<endpoint>' (because they are always prefixed themselves with a
# '/') and that is not equivalent to '/<endpoint'.
api = Api(app,
          version='1.0',
          title='Playing Card Deck API',
          description='A Simple REST Playing Card Deck API',
          prefix='/api')


# This collects the API operations into named groups under a root URL.
deck_ns = api.namespace('deck', description='Card deck related operations')
schema_ns = api.namespace('schema', description="This API's schema operations")

# Specifications of the objects accepted/returned by the API.
DeckId = api.model('Deck ID', {
    'id': fields.Integer(required=True, description='Deck ID', example=12345),
})


@schema_ns.route('')
class SchemaResource(Resource):
    """Resource allowing access to the OpenAPI schema for the entire API."""

    def get(self):
        """Return the OpenAPI schema."""
        log.debug("Generating schema")
        return api.__schema__


@deck_ns.route('')
class DeckCollection(Resource):
    """ Collection resource containing all decks. """

    @api.marshal_list_with(DeckId)
    def get(self):
        """Returns the list of deck ids."""
        log.debug("Listing all decks")
        return []


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='REST Playing Card Deck')
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

    app.run(host=args.host, port=args.port)
