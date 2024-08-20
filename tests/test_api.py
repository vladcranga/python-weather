"""
Unit tests for the WeatherAPI class.
"""
import unittest
from unittest.mock import patch, Mock
from weather.api import WeatherAPI

class TestWeatherAPI(unittest.TestCase):
    """
    Test cases for the WeatherAPI class.
    """
    @patch("weather.api.requests.get")
    def test_get_weather_success(self, mock_get):
        """
        Test the get_weather method with a successful API response.
        """
        # Simulate the API call's JSON response
        mock_response = Mock()
        mock_response.json.return_value = {
            "name": "Sacramento",
            "main": {"temp": 19},
            "weather": [{"description": "clear sky", "icon": "01d"}]
        }
        mock_get.return_value = mock_response
        
        api = WeatherAPI()
        result = api.get_weather(0, 0)
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Sacramento")
        self.assertEqual(result[1], 19)
        self.assertEqual(result[2], "clear sky")

    @patch("weather.api.requests.get")
    def test_get_weather_failure(self, mock_get):
        """
        Test the get_weather method with a failed API response.
        """
        mock_get.side_effect = Exception("Failed API call.")
        
        api = WeatherAPI()
        result = api.get_weather(0, 0)
        
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
