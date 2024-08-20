"""
Integration tests for the application.
"""
import unittest
from weather.api import WeatherAPI
from weather.data import get_coordinates_from_city

class TestIntegration(unittest.TestCase):
    """
    Integration test cases for the application.
    """
    def test_real_weather_api_call(self):
        """
        Test a real Weather API call.
        """
        api = WeatherAPI()
        # Coordinates for San Francisco
        result = api.get_weather(37.7749, -122.4194)  
        self.assertIsNotNone(result)
        self.assertIn("San Francisco", result[0])

    def test_real_get_coordinates_call(self):
        """
        Test the real get_coordinates_from_city call.
        """
        latitude, longitude = get_coordinates_from_city("San Francisco")
        self.assertIsNotNone(latitude)
        self.assertIsNotNone(longitude)
        self.assertAlmostEqual(latitude, 37.7749, places=1)
        self.assertAlmostEqual(longitude, -122.4194, places=1)

if __name__ == "__main__":
    unittest.main()
