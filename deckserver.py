'''
Webserver to provide card deck API.
'''
import logging

from flask import Flask
from flask_restplus import Resource, Api, fields

import deckstore

log = logging.getLogger(__name__)

app = Flask(__name__)

# Use a non-empty 'prefix' (becomes swagger 'basePath') for interop reasons -
# if it's empty then the basePath is '/', which with an API enpoint appended
# becomes '//<endpoint>' (because they are always prefixed themselves with a
# '/') and that is not equivalent to '/<endpoint'.
API_URL_PREFIX = '/api'
api = Api(app,
          version='1.0',
          title='Playing Card Deck API',
          description='A Simple REST Playing Card Deck API',
          prefix=API_URL_PREFIX)


# This collects the API operations into named groups under a root URL.
deck_ns = api.namespace('decks', description='Card deck related operations')
schema_ns = api.namespace('schema', description="This API's schema operations")

# Specifications of the objects accepted/returned by the API.
DeckId = api.model('Deck ID', {
    'id': fields.Integer(required=True, description='Deck ID', example=12345),
})

DeckCardsRemaining = api.model('Cards Remaining', {
    'cards_remaining': fields.Integer(description='Cards Remaining'),
})

Deck = api.inherit('Deck', DeckId, DeckCardsRemaining)


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
        return [{"id": deck_id} for deck_id in deckstore.list_decks()]

    @api.marshal_with(DeckId)
    @api.response(201, 'Deck successfully created.')
    def post(self):
        """Creates a new deck."""
        deck_id = deckstore.new_deck()
        return {"id": deck_id}, 201


@deck_ns.route('/<deckid>')
@api.response(404, 'Deck not found.')
class AppsResource(Resource):
    """ Individual resources representing a deck. """

    @api.marshal_with(Deck)
    def get(self, deckid):
        """Returns the data for a deck."""
        log.debug("Getting deck: %r", deckid)
        deck_data = deckstore.get_deck(deckid)
        if deck_data is None:
            log.debug("No deck found")
            return None, 404
        else:
            log.debug("Found deck")
            return deck_data

    @api.response(204, 'Deck successfully deleted.')
    def delete(self, deckid):
        """Deletes a deck."""
        log.debug("Deleting deck: %r", deckid)
        deckstore.delete_deck(deckid)
        return None, 204
