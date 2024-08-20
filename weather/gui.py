import tkinter as tk
from tkinter import ttk
from weather.api import WeatherAPI
from weather.data import load_favourite_cities, save_to_favourites, get_coordinates_from_city
import logging
import webbrowser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Weather:
    """
    A class to create and manage the Weather Forecast GUI.

    Attributes:
        master (tk.Tk): The root window of the application.
        input_city (ttk.Entry): Entry widget for the city name.
        input_latitude (ttk.Entry): Entry widget for the latitude.
        input_longitude (ttk.Entry): Entry widget for the longitude.
        favourite_cities (ttk.Combobox): Combobox for selecting the saved favourite cities.
        weather_info (tk.StringVar): Variable to display the weather information.
        icon_label (ttk.Label): Label widget to display the weather icon.
        forecast_tree (ttk.Treeview): Treeview widget to display the weather forecast.
    """

    def __init__(self, master):
        """Initialises the application and sets up the widgets."""
        self.master = master
        self.master.title("Weather Forecast")
        self.master.geometry("700x550")
        self.master.configure(bg="#f0f0f0")
        self.center_window()

        self.create_widgets()

    def center_window(self):
        """Centers the window on app launch."""
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - int((height // 1.8))
        self.master.geometry("{}x{}+{}+{}".format(width, height, x, y))

    def create_widgets(self):
        """Creates and arranges the GUI widgets."""
        self.frame = ttk.Frame(self.master, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.resizable(False, False)

        # Configure styles
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 11))
        style.configure("TEntry", font=("Arial", 11))

        # Create and place input fields
        ttk.Label(self.frame, text="City:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.input_city = ttk.Entry(self.frame, width=30)
        self.input_city.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(0, 10))

        ttk.Label(self.frame, text="Latitude:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.input_latitude = ttk.Entry(self.frame, width=30)
        self.input_latitude.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(0, 10))

        ttk.Label(self.frame, text="Longitude:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.input_longitude = ttk.Entry(self.frame, width=30)
        self.input_longitude.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(0, 10))

        # Create and place buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Show Weather", command=self.show_weather).grid(
            row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save to Favourites", command=self.save_to_favourites).grid(
            row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Get Coordinates", command=self.get_coordinates).grid(
            row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Quit", command=self.quit_app).grid(
            row=0, column=3, padx=5)

        # Create and place favourite cities list
        ttk.Label(self.frame, text="Favourite Cities:").grid(row=4, column=0, sticky=tk.W, pady=10)
        self.favourite_cities = ttk.Combobox(self.frame, state="readonly")
        self.favourite_cities.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(0, 10))
        self.load_favourite_cities()
        self.favourite_cities.bind("<<ComboboxSelected>>", self.load_favourite_location)

        # Create and place weather information
        self.weather_frame = ttk.Frame(self.frame)
        self.weather_frame.grid(row=5, column=0, columnspan=2, pady=20)

        self.weather_info = tk.StringVar()
        ttk.Label(self.weather_frame, textvariable=self.weather_info, wraplength=500, justify="left").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.icon_label = ttk.Label(self.weather_frame)
        self.icon_label.grid(row=0, column=1, padx=10, pady=10)

        # Create forecast frame
        self.forecast_frame = ttk.Frame(self.frame)
        self.forecast_frame.grid(row=6, column=0, columnspan=2, pady=20)

        # Create and place forecast information
        self.forecast_tree = ttk.Treeview(
            self.forecast_frame, columns=(
                "Date", "Temperature", "Description"), show="headings", height=6)
        self.forecast_tree.heading("Date", text="Date (DD/MM/YYYY)")
        self.forecast_tree.heading("Temperature", text="Temperature")
        self.forecast_tree.heading("Description", text="Description")

        self.forecast_tree.column("Date", anchor="center")
        self.forecast_tree.column("Temperature", anchor="center")
        self.forecast_tree.column("Description", anchor="center")

        self.forecast_tree.pack()

    def load_favourite_cities(self):
        """
        Loads the favourite cities from a file into the combobox.

        If the file is not found or an error occurs, a message is displayed to the user.
        """
        cities = load_favourite_cities()
        if cities:
            self.favourite_cities["values"] = ["Select a city"] + cities
            self.favourite_cities.set("Select a city")
        else:
            self.favourite_cities["values"] = ["Unable to load cities"]
            self.weather_info.set("Favourites file not found. No saved cities available.")
            logging.error("Failed to load favourite cities. Favourites file not found.")

    def load_favourite_location(self, event):
        """
        Loads the latitude and longitude for the selected favourite location.

        Args:
            event: The event object triggered by selecting a city from the combobox.
        """
        city = self.favourite_cities.get()
        if city != "Select a city":
            self.input_city.delete(0, tk.END)
            self.input_city.insert(0, city)

    def save_to_favourites(self):
        """
        Saves the current city to the favourites list.

        If the city name is invalid or empty, a message is displayed to the user.
        """
        city = self.input_city.get().strip()
        if not city or not city.replace(" ", "").isalpha():
            self.weather_info.set("Please enter a valid city name.")
            logging.warning("Attempted to save an invalid city name.")
            return
        if save_to_favourites(city):
            self.load_favourite_cities()
            self.favourite_cities.set(city)
        else:
            self.weather_info.set("Error saving to favourites file. Please try again later.")
            logging.error("Failed to save city to favourites.")

    def show_weather(self):
        """
        Retrieves and displays weather information for the specified city or coordinates.

        The weather information includes the current temperature, description,
        and a weather icon. If the input is invalid or the data cannot be retrieved,
        an error message is displayed.
        """
        city = self.input_city.get().strip()
        latitude = self.input_latitude.get().strip()
        longitude = self.input_longitude.get().strip()

        if city and city.replace(" ", "").isalpha():
            latitude, longitude = get_coordinates_from_city(city)
            if not latitude or not longitude:
                return
        elif not latitude or not longitude:
            self.weather_info.set("Please enter a valid city name or both a latitude and longitude.")
            logging.warning("Invalid city, latitude, or longitude input.")
            return

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            self.weather_info.set("Invalid latitude or longitude. Please enter numeric values.")
            logging.warning("Invalid latitude or longitude input.")
            return

        weather_api = WeatherAPI()
        weather_data = weather_api.get_weather(latitude, longitude)
        if weather_data is not None:
            city, temperature_celsius, description, icon_data = weather_data
            temperature_fahrenheit = (temperature_celsius * 9/5) + 32
            self.icon_image = tk.PhotoImage(data=icon_data)
            self.icon_label.configure(image=self.icon_image)

            information = (
            f"The current temperature in {city} is {temperature_celsius:.1f}°C / {temperature_fahrenheit:.1f}°F.\n"
            f"Additional details: {description}."
            )
            self.weather_info.set(information)
            self.show_forecast(latitude, longitude)
        else:
            self.weather_info.set("An unexpected error occurred. Please try again later.")
            logging.error("Could not retrieve the weather information.")

    def show_forecast(self, latitude, longitude):
        """
        Retrieves and displays forecast information for the specified coordinates.

        The forecast includes the date, temperature, and a brief weather description.
        """
        weather_api = WeatherAPI()
        forecast_data = weather_api.get_forecast(latitude, longitude)
        if forecast_data:
            # Clear previous forecast data
            for row in self.forecast_tree.get_children():
                self.forecast_tree.delete(row)

            for date, (temperature_celsius, description) in forecast_data.items():
                temperature_fahrenheit = (temperature_celsius * 9/5) + 32
                self.forecast_tree.insert("", "end", values=(
                    date, f"{temperature_celsius:.1f}°C / {temperature_fahrenheit:.1f}°F", description))
        else:
            self.weather_info.set(f"{self.weather_info.get()}\nCould not retrieve the forecast.")
            logging.error("Could not retrieve the forecast information.")

    def get_coordinates(self):
        """Opens a website to help find coordinates."""
        webbrowser.open("https://latlong.net")

    def quit_app(self):
        """Closes the app."""
        self.master.quit()
