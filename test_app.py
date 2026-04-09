import unittest
import json
from app import app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_home(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # Check for the new title!
        self.assertTrue(b'ML-Ops Sentiment Engine' in response.data)

    def test_analyze_endpoint(self):
        # Test the NLP API secretly
        response = self.tester.post('/analyze', 
                                    data=json.dumps({'text': 'I am extremely happy today!'}),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sentiment'], 'Positive')

if __name__ == '__main__':
    unittest.main()