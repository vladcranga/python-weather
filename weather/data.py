# data.py
from weather.api import WeatherAPI
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_favourite_cities():
    """Loads favourite cities from a file."""
    try:
        with open("favourites.txt", "r") as file:
            cities = file.readlines()
            return [city.strip() for city in cities]
    except FileNotFoundError:
        return None
    except IOError as e:
        logging.error(f"File error: {e}")
        return None

def save_to_favourites(city):
    """Saves the current city to the favourites list."""
    try:
        with open("favourites.txt", "a") as file:
            file.write(f"{city}\n")
        return True
    except IOError as e:
        logging.error(f"File error: {e}")
        return False

def get_coordinates_from_city(city):
    """Returns coordinates based on the provided city name."""
    api_key = WeatherAPI().get_api_key()
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None, None

        return data[0]["lat"], data[0]["lon"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None, None
    except ValueError as e:
        logging.error(f"Data error: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None, None
