'''
Webserver to provide card deck API.
'''
import logging

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
deck_ns = api.namespace('decks', description='Card deck related operations')
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

    @api.marshal_with(DeckId)
    @api.response(201, 'Deck successfully created.')
    def post(self):
        """Creates a new deck."""
        # create_category(request.json)
        return {"id": 1}, 201
