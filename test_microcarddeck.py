import logging
import unittest
import json
import responses
import re

import microcarddeck
import deckstore

DATASTORE_URL_BASE = 'http://127.0.0.1:5000/api'
CONTENT_TYPE_JSON = 'application/json'


class MicroCardDeckTestCase(unittest.TestCase):

    def setUp(self):
        # Disable the error catching during request handling so that you get
        # better error reports.
        microcarddeck.app.config['TESTING'] = True

        self.app = microcarddeck.app.test_client()

        deckstore.init('test_schema.json')

        self.url_prefix = "/api"

    def tearDown(self):
        deckstore.term()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_schema(self):
        rv = self.app.get(self.url_prefix + '/schema')
        self.assertEqual(rv.status_code, 200)

    def test_decks_collection_empty(self):
        rv = self.app.get(self.url_prefix + '/decks')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), [])

    @responses.activate
    def test_decks_collection_create(self):
        url_re = re.compile(DATASTORE_URL_BASE + r'/apps/\d+')
        responses.add(responses.PUT, url_re,
                      body=None, status=204,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.post(self.url_prefix + '/decks')
        self.assertEqual(rv.status_code, 201)
        response_data = json.loads(rv.data.decode())
        self.assertIsInstance(response_data.get("id"), int)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s:%(funcName)s:%(message)s',
                        level=logging.INFO)
    logging.getLogger("pyswagger").setLevel(logging.WARNING)
    unittest.main()
