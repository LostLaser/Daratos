import unittest

from tests import helper
from app import app

class TextTestCases(unittest.TestCase):
    def test_blank_extract(self):
        tester = app.test_client(self)
        response = tester.post('/extract/html', json = helper.html_from_file("test_articles/article_blank.txt"))
        json_data = response.get_json()
        
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response)

    def test_extract_cnn(self):
        tester = app.test_client(self)
        response = tester.post('/extract/html', json = helper.html_from_file("test_articles/article_cnn_1.txt"))
        json_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("The price tag for that" in json_data["content"])

    def test_extract_fox(self):
        tester = app.test_client(self)
        response = tester.post('/extract/html', json = helper.html_from_file("test_articles/article_fox_1.txt"))
        json_data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("The high court also backed Republicans over the liberal" in json_data["content"])

if __name__ == '__main__':
    unittest.main()