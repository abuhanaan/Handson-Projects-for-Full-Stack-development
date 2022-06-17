#Import all dependencies
import unittest
import json
from flaskr import create_app
from models import setup_db

class BookShelfTestCase(unittest.TestCase):
    """This class represents the ___ test case"""  
    self.app = create_app()
    self.client = self.app.test_client()
    self.database_name = "bookshelf_test"
    self.database_path = "postgres://{}{}@{}/{}".format(
                            'student', 'student', 'localhost:5432', self.database_name)
    setup_db(app, self.database_path)

    self.new_book = {
        'title': 'How to Ride to London From Nigeria',
        'author': 'Qomorudeen Mustopha',
        'rating': 5
    }

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        self.client = app.test_client
        pass

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
