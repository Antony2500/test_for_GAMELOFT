import unittest
from app.routes.api import get_forums, get_join_forms, get_messages
from app import create_app
import json
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))


app_dir = os.path.join(current_dir, '..')
sys.path.append(app_dir)

class TestAPIRoutes(unittest.TestCase):

    def setUp(self):
        app = create_app()
        self.app = app.test_client()

    def test_get_forums(self):
        response = self.app.get('/forums')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) > 0)  

    def test_get_join_forms(self):
        response = self.app.get('/join_forms')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) > 0) 

    def test_get_messages(self):
        response = self.app.get('/forums/1/messages')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['forum_messages']) > 0) 
if __name__ == '__main__':
    unittest.main()
