"""
Unit tests for the GUI.
"""
import unittest
from unittest.mock import patch, Mock
from tkinter import Tk
from weather.gui import Weather
import time

class TestWeatherGUI(unittest.TestCase):
    """
    Test cases for the GUI.
    """
    def setUp(self):
        """
        Set up the test environment.
        """
        self.root = Tk()
        self.app = Weather(self.root)

    def tearDown(self):
        """
        Clean up the test environment.
        """
        self.root.update_idletasks()
        self.root.destroy()
        time.sleep(0.1)

    @patch("weather.gui.WeatherAPI.get_weather")
    def test_show_weather_success(self, mock_get_weather):
        """
        Test the show_weather method with a successful API response.
        """
        # Simulate the API response
        image_data = b"R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="
        mock_get_weather.return_value = ("Austin", 34, "clear sky", image_data)
        self.app.input_city.insert(0, "Austin")
        self.app.show_weather()
        
        self.assertIn("Austin", self.app.weather_info.get())

    @patch("weather.gui.WeatherAPI.get_weather")
    def test_show_weather_failure(self, mock_get_weather):
        """
        Test the show_weather method with a failed API response.
        """
        # Simulate an API failure
        mock_get_weather.return_value = None
        self.app.input_city.insert(0, "City")
        self.app.show_weather()
        
        self.assertEqual(self.app.weather_info.get(), "An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    unittest.main()
