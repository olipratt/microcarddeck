import uuid

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client


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

        # Create a client which will send requests
        self._client = Client(Security(self._app))

    def new_deck(self):
        """Create a new deck, and return its ID."""
        deck_id = uuid.uuid1().int

        self._client.request(self._put_deck_data(appid=deck_id,
                                                 payload={"data": {}}))

        return deck_id


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
    global client

    return connection.new_deck()
