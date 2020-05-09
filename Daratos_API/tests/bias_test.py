import unittest
import os
import sys

from app import app

class BiasTestCases(unittest.TestCase):
    def html_from_file(self, relative_file_path):
        script_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        with open(os.path.join(script_location, relative_file_path), "r", encoding = "utf8") as html_file:
            return {"raw_html": html_file.read()}

    def test_bias_cnn(self):
        tester = app.test_client(self)
        response = tester.post('/bias/html', json = self.html_from_file("test_articles/article_cnn_1.html"))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
