import unittest

from tests import helper
from app import app

class BiasTestCases(unittest.TestCase):
    def test_bias_cnn(self):
        tester = app.test_client(self)
        response = tester.post('/bias/html', json = helper.html_from_file("test_articles/article_cnn_1.html"))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
