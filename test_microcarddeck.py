import logging
import unittest
import json
import responses
import re

import deckserver

DATASTORE_SCHEMA_PATH = 'test_schema.json'
DATASTORE_URL_BASE = 'http://127.0.0.1:5000/api'
CONTENT_TYPE_JSON = 'application/json'


class MicroCardDeckTestCase(unittest.TestCase):

    def setUp(self):
        # Disable the error catching during request handling so that you get
        # better error reports.
        deckserver.app.config['TESTING'] = True

        deckserver.assign_data_store(DATASTORE_SCHEMA_PATH)
        self.app = deckserver.app.test_client()

    def tearDown(self):
        # No teardown of test fixtures required.
        pass

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_schema(self):
        rv = self.app.get(deckserver.API_URL_PREFIX + '/schema')
        self.assertEqual(rv.status_code, 200)

    @responses.activate
    def test_decks_collection_empty(self):
        responses.add(responses.GET, DATASTORE_URL_BASE + '/apps',
                      body="[]", status=200,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.get(deckserver.API_URL_PREFIX + '/decks')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), [])

    @responses.activate
    def test_decks_collection_populated(self):
        datastore_response = [{"name": "12345"}, {"name": "67890"}]
        deckserver_response = [{"id": 12345}, {"id": 67890}]
        responses.add(responses.GET, DATASTORE_URL_BASE + '/apps',
                      json=datastore_response, status=200,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.get(deckserver.API_URL_PREFIX + '/decks')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), deckserver_response)

    @responses.activate
    def test_decks_collection_create(self):
        url_re = re.compile(DATASTORE_URL_BASE + r'/apps/\d+')
        responses.add(responses.PUT, url_re,
                      body=None, status=204,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.post(deckserver.API_URL_PREFIX + '/decks')
        self.assertEqual(rv.status_code, 201)
        response_data = json.loads(rv.data.decode())
        self.assertIsInstance(response_data.get("id"), int)

    @responses.activate
    def test_decks_resource_get_success(self):
        datastore_response = {"name": "12345", "data": {}}
        deckserver_response = {"id": 12345, "cards_remaining": 0}
        responses.add(responses.GET, DATASTORE_URL_BASE + '/apps/12345',
                      json=datastore_response, status=200,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.get(deckserver.API_URL_PREFIX + '/decks/12345')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), deckserver_response)

    @responses.activate
    def test_decks_resource_get_failure(self):
        responses.add(responses.GET, DATASTORE_URL_BASE + '/apps/12345',
                      body=None, status=404,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.get(deckserver.API_URL_PREFIX + '/decks/12345')
        self.assertEqual(rv.status_code, 404)

    @responses.activate
    def test_decks_resource_delete(self):
        responses.add(responses.DELETE, DATASTORE_URL_BASE + '/apps/12345',
                      body=None, status=204,
                      content_type=CONTENT_TYPE_JSON)

        rv = self.app.delete(deckserver.API_URL_PREFIX + '/decks/12345')
        self.assertEqual(rv.status_code, 204)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s:%(funcName)s:%(message)s',
                        level=logging.INFO)
    unittest.main()
