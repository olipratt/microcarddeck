import logging
import uuid

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
# pyswagger makes INFO level logs regularly by default, so lower its logging
# level to prevent the spam.
logging.getLogger("pyswagger").setLevel(logging.WARNING)


log = logging.getLogger(__name__)


class DeckStore:
    """Definition of the datastore which client connections are made to."""

    def __init__(self, schema_path):
        """Create a deck store.

        :param schema_path: The url or file path of the swagger schema of the
                            datastore to use.
        :type schema_path: str.
        """
        # Load Swagger schema.
        self._app = App.create(schema_path)

        # Expose references to API calls that will be used.
        # These are functions that return correctly formatted requests for
        # client instances to send on to the server.
        self.get_decks_list = self._app.op['get_apps_collection']
        self.put_deck_data = self._app.op['put_apps_resource']
        self.get_deck = self._app.op['get_apps_resource']
        self.delete_deck = self._app.op['delete_apps_resource']


class DeckStoreClient:

    def __init__(self, deck_store):
        """Create a new client to access the deck store.

        :param deck_store: The definition of the store to connect to.
        :type schema_path: DeckStore.
        """
        # Load Swagger schema.
        self._deck_store = deck_store

        # Create a client which will send requests
        self._client = Client(Security(self._deck_store))

    def new_deck(self):
        """Create a new deck, and return its ID."""
        # Just give each deck a truncated integer UUID as an ID for now.
        # Use uuid4 as that's random, and hopefully won't collide in test use
        # which is all this is really for.
        deck_id = uuid.uuid4().int % 100000000
        log.debug("Creating new deck with ID: %r", deck_id)

        prepared_request = self._deck_store.put_deck_data(appid=deck_id,
                                                          payload={"data": {}})
        resp = self._client.request(prepared_request)
        assert resp.status == 204
        log.debug("Deck created successfully")

        return deck_id

    def list_decks(self):
        """Get a list of all deck IDs in the store."""
        prepared_request = self._deck_store.get_decks_list()
        resp = self._client.request(prepared_request)
        assert resp.status == 200

        response_data = resp.data
        deck_ids = [int(entry.name) for entry in response_data]
        log.debug("Found decks as: %r", deck_ids)
        return deck_ids

    def get_deck(self, deck_id):
        """Get a single deck by ID, or None if it does not exist."""
        log.debug("Getting deck: %r", deck_id)
        prepared_request = self._deck_store.get_deck(appid=deck_id)
        resp = self._client.request(prepared_request)
        if resp.status == 200:
            return {"id": resp.data.name, "cards_remaining": 0}
        else:
            return None

    def delete_deck(self, deck_id):
        """Delete a single deck by ID."""
        log.debug("Deleting deck: %r", deck_id)
        prepared_request = self._deck_store.delete_deck(appid=deck_id)
        resp = self._client.request(prepared_request)
        assert resp.status == 204
