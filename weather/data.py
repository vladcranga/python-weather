from weather.api import WeatherAPI
import sys
import os
import shutil
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_file_path(filename, for_writing=False):
    """Returns the correct path for a file in both normal and PyInstaller environments.
    
    Args:
        filename (str): The name of the file to get the path for.
        for_writing (bool): Whether the path is intended for writing (use user data directory).
    
    Returns:
        str: The absolute path to the requested file.
    """
    if for_writing:
        user_home = os.path.expanduser("~")
        app_data_folder = os.path.join(user_home, ".python_weather_app")
        os.makedirs(app_data_folder, exist_ok=True)
        return os.path.join(app_data_folder, filename)

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, filename)

def load_favourite_cities():
    """
    Loads favourite cities from a file.

    Returns:
        list of str: A list of city names, if the file is found and read successfully.
        None: If the file is not found or an error occurs during reading.
    """
    try:
        persistent_file_path = get_file_path("favourites.txt", for_writing=True)
        if not os.path.exists(persistent_file_path):
            bundled_file_path = get_file_path("favourites.txt")
            shutil.copy(bundled_file_path, persistent_file_path)
        with open(persistent_file_path, "r") as file:
            cities = file.readlines()
            return [city.strip() for city in cities]
    except FileNotFoundError:
        logging.warning("Favourites file not found.")
        return []
    except IOError as e:
        logging.error(f"File error: {e}")
        return []

def save_to_favourites(city):
    """
    Saves the specified city to the favourites list.

    Args:
        city (str): The name of the city to save to the favourites list.

    Returns:
        bool: True if the city was saved successfully, False if an error occurred.
    """
    try:
        file_path = get_file_path("favourites.txt", for_writing=True)
        with open(file_path, "a") as file:
            file.write(f"{city}\n")
        return True
    except IOError as e:
        logging.error(f"File error: {e}")
        return False

def get_coordinates_from_city(city):
    """
    Returns coordinates based on the provided city name, using the OpenWeatherMap API.

    Args:
        city (str): The name of the city to retrieve coordinates for.

    Returns:
        tuple: A tuple containing latitude and longitude as floats, or (None, None) if the
        city is not found or an error occurs.
    """
    api_key = WeatherAPI().get_api_key()
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=1&appid={api_key}"
    )
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
