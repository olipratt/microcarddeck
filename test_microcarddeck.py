import logging
import unittest
import json
import responses
import re

import microcarddeck
import deckstore
from deckserver import API_URL_PREFIX

DATASTORE_SCHEMA_PATH = 'test_schema.json'
DATASTORE_URL_BASE = 'http://127.0.0.1:5000/api'
CONTENT_TYPE_JSON = 'application/json'


class MicroCardDeckTestCase(unittest.TestCase):

    def setUp(self):
        # Disable the error catching during request handling so that you get
        # better error reports.
        microcarddeck.app.config['TESTING'] = True

        deckstore.init(DATASTORE_SCHEMA_PATH)
        self.app = microcarddeck.app.test_client()

    def tearDown(self):
        deckstore.term()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_schema(self):
        rv = self.app.get(API_URL_PREFIX + '/schema')
        self.assertEqual(rv.status_code, 200)

    @responses.activate
    def test_decks_collection_empty(self):
        responses.add(responses.GET, DATASTORE_URL_BASE + '/apps',
                      body="[]", status=200,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.get(API_URL_PREFIX + '/decks')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), [])

    @responses.activate
    def test_decks_collection_populated(self):
        datastore_response = [{"name": "12345"}, {"name": "67890"}]
        deckserver_response = [{"id": 12345}, {"id": 67890}]
        responses.add(responses.GET, DATASTORE_URL_BASE + '/apps',
                      json=datastore_response, status=200,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.get(API_URL_PREFIX + '/decks')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), deckserver_response)

    @responses.activate
    def test_decks_collection_create(self):
        url_re = re.compile(DATASTORE_URL_BASE + r'/apps/\d+')
        responses.add(responses.PUT, url_re,
                      body=None, status=204,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.post(API_URL_PREFIX + '/decks')
        self.assertEqual(rv.status_code, 201)
        response_data = json.loads(rv.data.decode())
        self.assertIsInstance(response_data.get("id"), int)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s:%(funcName)s:%(message)s',
                        level=logging.INFO)
    logging.getLogger("pyswagger").setLevel(logging.WARNING)
    unittest.main()
