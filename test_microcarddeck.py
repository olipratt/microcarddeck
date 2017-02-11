import logging
import unittest
import json

import microcarddeck

CONTENT_TYPE_JSON = 'application/json'


class MicroCardDeckTestCase(unittest.TestCase):

    def setUp(self):
        # Disable the error catching during request handling so that you get
        # better error reports.
        microcarddeck.app.config['TESTING'] = True

        self.app = microcarddeck.app.test_client()

        self.url_prefix = "/api"

    def tearDown(self):
        pass

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_schema(self):
        rv = self.app.get(self.url_prefix + '/schema')
        self.assertEqual(rv.status_code, 200)

    def test_decks_collection_empty(self):
        rv = self.app.get(self.url_prefix + '/deck')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode()), [])


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s:%(message)s',
                        level=logging.INFO)
    unittest.main()
