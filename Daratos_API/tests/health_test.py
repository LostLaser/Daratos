import unittest

from app import app

class TextTestCases(unittest.TestCase):
    def test_health(self):
        tester = app.test_client(self)
        response = tester.get('/health', content_type='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"UP" in response.data)

if __name__ == '__main__':
    unittest.main()
