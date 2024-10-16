import unittest
import json
from app import app  # Ensure this matches your app file name

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def test_home(self):
        """Test the home page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!doctype html>', response.data)  # Check if HTML is returned

    def test_predict(self):
        """Test the predict endpoint"""
        # Prepare sample input data
        sample_data = {
            "protein": 30,
            "carbs": 50,
            "fat": 20
        }
        
        response = self.app.post('/predict', data=json.dumps(sample_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check if response is in JSON format
        self.assertEqual(response.content_type, 'application/json')

        # Check that results are returned
        results = json.loads(response.data)
        self.assertIsInstance(results, list)  # Ensure results are a list
        if results:
            self.assertIn('Recipe_name', results[0])  # Check if the first result has Recipe_name

if __name__ == '__main__':
    unittest.main()
