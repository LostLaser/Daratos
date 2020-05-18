import unittest

from tests import helper
from app import app

class BiasTestCases(unittest.TestCase):
    def test_bias_cnn(self):
        tester = app.test_client(self)
        response = tester.post('/bias/html', json = helper.html_from_file("test_articles/article_cnn_1.txt"))
        json_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data["total_bias"], "moderately left")
        

    def test_extract_fox(self):
        tester = app.test_client(self)
        response = tester.post('/bias/html', json = helper.html_from_file("test_articles/article_fox_1.txt"))
        json_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data["total_bias"], "neutral")

if __name__ == '__main__':
    unittest.main()
