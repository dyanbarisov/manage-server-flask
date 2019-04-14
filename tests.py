import unittest

from werkzeug.exceptions import NotFound, HTTPException

from api import RackResource
from mock import patch
from api import app


class Tests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch('db.Session.query')
    def test_get_rack(self, session_mock):
        session_mock.return_value.filter.return_value.first.return_value = {'id': 1}
        rack_resource = RackResource()
        result = rack_resource.get(id=1)
        self.assertEqual(result['id'], 1)

    @patch('db.Session.query')
    def test_get_rack_fail(self, session_mock):
        session_mock.return_value.filter.return_value.first.return_value = None
        rack_resource = RackResource()
        with self.assertRaises(HTTPException) as context:
            result = rack_resource.get(id=1)


if __name__ == "__main__":
    unittest.main()
