import tkinter as tk
import logging
import requests
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class WeatherAPI:
    """
    A class that interacts with the OpenWeatherMap API to retrieve current weather
    and forecast data.

    Attributes:
        api_key (str): The API key used to authenticate with the OpenWeatherMap API.
    """

    def __init__(self):
        """
        Initialises the WeatherAPI instance by loading the API key.
        """
        self.api_key = self.get_api_key()

    def get_api_key(self):
        """
        Retrieves the API key from the config.json file.

        Returns:
            str: The API key, when retrieved successfully.
            None: If the API key is not found or an error occurs.

        Raises:
            ValueError: If the API key is empty.
        """
        try:
            with open("config.json", "r") as config_file:
                api_key = json.load(config_file)["api_key"]
                if not api_key:
                    raise ValueError("The API key is empty.")
                return api_key
        except FileNotFoundError:
            logging.error("The configuration file 'config.json' was not found.")
            return None
        except ValueError as e:
            logging.error(f"Error: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def get_weather(self, latitude, longitude):
        """
        Retrieves current weather data for the specified coordinates.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            tuple: A tuple containing the city name (str), temperature (float),
            weather description (str), and weather icon data (bytes).
            None: If an error occurs during the API request.

        Raises:
            requests.exceptions.RequestException: If there is a network error.
            ValueError: If the response data is invalid.
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            city = data.get("name", "your selected location")
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]

            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_data = requests.get(icon_url).content

            return city, temperature, description, icon_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return None
        except ValueError as e:
            logging.error(f"Data error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None

    def get_forecast(self, latitude, longitude):
        """
        Retrieves a five-day weather forecast for the specified coordinates.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            dict: A dictionary where keys are dates (str) and values are tuples
            containing the temperature (float) and weather description (str).
            None: If an error occurs during the API request.

        Raises:
            requests.exceptions.RequestException: If there is a network error.
            ValueError: If the response data is invalid.
        """
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            forecast_data = response.json()

            daily_forecasts = {}
            today = datetime.now().strftime("%d-%m-%Y")

            for item in forecast_data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%d-%m-%Y")

                if date == today:
                    continue

                if date not in daily_forecasts:
                    temperature = item["main"]["temp"]
                    description = item["weather"][0]["description"]
                    daily_forecasts[date] = (temperature, description)

            return daily_forecasts
        except Exception as e:
            logging.error(f"Error: {e}")
            return None
