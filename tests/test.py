import unittest
import json
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """Test the home page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Diet Food Suggestion', response.data)

    def test_predict(self):
        """Test the predict endpoint."""
        # Define the input data
        input_data = {
            'protein': 30,
            'carbs': 50,
            'fat': 20
        }

        # Send a POST request to the /predict endpoint
        response = self.app.post('/predict', data=json.dumps(input_data), content_type='application/json')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the response data
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn('Recipe_name', data[0])
        self.assertIn('Diet_type', data[0])
        self.assertIn('Cuisine_type', data[0])
        self.assertIn('Protein(g)', data[0])
        self.assertIn('Carbs(g)', data[0])
        self.assertIn('Fat(g)', data[0])

if __name__ == '__main__':
    unittest.main()
