import logging
import uuid

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client


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
        self._put_deck_data = self._app.op['put_apps_resource']
        self._get_decks_list = self._app.op['get_apps_collection']

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
        response_data = self._client.request(self._get_decks_list()).data
        log.debug("Found decks as: %r", response_data)
        return response_data


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
