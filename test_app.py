import unittest
from app import app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_home(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Live Production Telemetry' in response.data)

    def test_metrics_api(self):
        response = self.tester.get('/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'cpu' in response.data)
        self.assertTrue(b'ram' in response.data)

if __name__ == '__main__':
    unittest.main()