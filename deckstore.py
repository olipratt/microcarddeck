import logging
import uuid

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
# pyswagger makes INFO level logs regularly by default, so lower its logging
# level to prevent the spam.
logging.getLogger("pyswagger").setLevel(logging.WARNING)


log = logging.getLogger(__name__)


connection = None


class DeckStoreConnection():

    def __init__(self, schema_path):
        """Create a new connection to the deck store.

        :param schema_path: The url or file path of the swagger schema of the
                            datastore to use.
        :type schema_path: str.

        """
        # Load Swagger schema.
        self._app = App.create(schema_path)

        # Prepare references to API calls that will be used.
        self._get_decks_list = self._app.op['get_apps_collection']
        self._put_deck_data = self._app.op['put_apps_resource']
        self._get_deck = self._app.op['get_apps_resource']
        self._delete_deck = self._app.op['delete_apps_resource']

        # Create a client which will send requests
        self._client = Client(Security(self._app))

    def new_deck(self):
        """Create a new deck, and return its ID."""
        deck_id = uuid.uuid1().int
        log.debug("Creating new deck with ID: %r", deck_id)

        resp = self._client.request(self._put_deck_data(appid=deck_id,
                                                        payload={"data": {}}))
        assert resp.status == 204
        log.debug("Deck created successfully")

        return deck_id

    def list_decks(self):
        resp = self._client.request(self._get_decks_list())
        assert resp.status == 200

        response_data = resp.data
        deck_ids = [int(entry.name) for entry in response_data]
        log.debug("Found decks as: %r", deck_ids)
        return deck_ids

    def get_deck(self, deck_id):
        log.debug("Getting deck: %r", deck_id)
        resp = self._client.request(self._get_deck(appid=deck_id))
        if resp.status == 200:
            return {"id": resp.data.name, "cards_remaining": 0}
        else:
            return None

    def delete_deck(self, deck_id):
        log.debug("Deleting deck: %r", deck_id)
        resp = self._client.request(self._delete_deck(appid=deck_id))
        assert resp.status == 204


def init(schema_path):
    """Initialise the deck store."""
    global connection
    assert connection is None

    # Create the client connection.
    connection = DeckStoreConnection(schema_path)


def term():
    """Terminate the deck store."""
    global connection
    connection = None


def new_deck():
    """Create a new deck, and return its ID."""
    global connection
    return connection.new_deck()


def list_decks():
    """List the IDs of all decks."""
    global connection
    return connection.list_decks()


def get_deck(deck_id):
    """Get a deck by ID."""
    global connection
    return connection.get_deck(deck_id)


def delete_deck(deck_id):
    """Delete a deck by ID."""
    global connection
    connection.delete_deck(deck_id)
