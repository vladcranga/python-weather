# test_integration.py
import unittest
from weather.api import WeatherAPI
from weather.data import get_coordinates_from_city

class TestIntegration(unittest.TestCase):

    def test_real_weather_api_call(self):
        api = WeatherAPI()
        # Coordinates for San Francisco
        result = api.get_weather(37.7749, -122.4194)  
        self.assertIsNotNone(result)
        self.assertIn("San Francisco", result[0])

    def test_real_get_coordinates_call(self):
        latitude, longitude = get_coordinates_from_city("San Francisco")
        self.assertIsNotNone(latitude)
        self.assertIsNotNone(longitude)
        self.assertAlmostEqual(latitude, 37.7749, places=1)
        self.assertAlmostEqual(longitude, -122.4194, places=1)

if __name__ == "__main__":
    unittest.main()
