# test_data.py
import unittest
from unittest.mock import Mock, mock_open, patch
from weather.data import load_favourite_cities, save_to_favourites, get_coordinates_from_city

class TestDataFunctions(unittest.TestCase):

    @patch("weather.data.open", new_callable=mock_open, read_data="New York\nDallas\n")
    def test_load_favourite_cities(self, mock_file):
        cities = load_favourite_cities()
        self.assertEqual(cities, ["New York", "Dallas"])

    @patch("weather.data.open", new_callable=mock_open)
    def test_save_to_favourites(self, mock_file):
        success = save_to_favourites("London")
        self.assertTrue(success)
        mock_file().write.assert_called_once_with("London\n")

    @patch("weather.data.requests.get")
    def test_get_coordinates_from_city_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{"lat": 123, "lon": 456}]
        mock_get.return_value = mock_response
        
        latitude, longitude = get_coordinates_from_city("TestCity")
        self.assertEqual(latitude, 123)
        self.assertEqual(longitude, 456)

    @patch("weather.data.requests.get")
    def test_get_coordinates_from_city_failure(self, mock_get):
        mock_get.side_effect = Exception("Failed API call.")
        
        latitude, longitude = get_coordinates_from_city("TestCity")
        self.assertIsNone(latitude)
        self.assertIsNone(longitude)

if __name__ == "__main__":
    unittest.main()