import unittest
from app import app

class BasicTestCase(unittest.TestCase):
    def test_home(self):
        # This creates a fake web browser to test our app natively
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        
        # 1. Check if the website loads without crashing (Status Code 200)
        self.assertEqual(response.status_code, 200)
        
        # 2. Check if our specific text is on the page
        self.assertTrue(b'DevOps Pipeline Active' in response.data)

if __name__ == '__main__':
    unittest.main()