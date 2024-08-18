# api.py
import tkinter as tk
import requests
from datetime import datetime

class WeatherAPI:
    def __init__(self):
        self.api_key = self.get_api_key()

    def get_api_key(self):
        """Retrieves the API key."""
        try:
            with open("api.txt", "r") as api_key_file:
                api_key = api_key_file.read().strip()
                if not api_key:
                    raise ValueError("The API key is empty.")
                return api_key
        except FileNotFoundError:
            print("The API key file 'api.txt' was not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_weather(self, latitude, longitude):
        """Retrieves weather data from the API."""
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
            print(f"Network error: {e}")
            return None
        except ValueError as e:
            print(f"Data error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_forecast(self, latitude, longitude):
        """Retrieves forecast data from the API."""
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
            print(f"Error: {e}")
            return None