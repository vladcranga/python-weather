# weather.py
# An app that displays the weather in a location.
# It uses the openweathermap API: https: / openweathermap.org/

import tkinter as tk
from tkinter import ttk
import requests
import json
import webbrowser
from datetime import datetime

class Weather:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather Forecast")
        self.master.geometry("700x500")
        self.master.configure(bg="#f0f0f0")

        self.create_widgets()
    
    def create_widgets(self):
        """Creates and arranges the GUI widgets."""
        self.frame = ttk.Frame(self.master, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)   

        # Configure styles
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 11))
        style.configure('TEntry', font=('Arial', 11))

        # Create and place input fields
        ttk.Label(self.frame, text="Latitude:").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.input_latitude = ttk.Entry(self.frame, width=30)
        self.input_latitude.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(0, 10))

        ttk.Label(self.frame, text="Longitude:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.input_longitude = ttk.Entry(self.frame, width=30)
        self.input_longitude.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(0, 10))

        # Create and place buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Show Weather", command=self.show_weather).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Get Coordinates", command=self.get_coordinates).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Quit", command=self.quit_app).grid(row=0, column=2, padx=5)

        # Create and place weather information
        self.weather_info = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.weather_info, wraplength=500, justify="center").grid(
            row=3, column=0, columnspan=2, pady=20)
        
        # Create forecast frame
        self.forecast_frame = ttk.Frame(self.frame)
        self.forecast_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Create and place forecast information
        self.forecast_tree = ttk.Treeview(
            self.forecast_frame, columns=("Date", "Temperature", "Description"), show="headings")
        self.forecast_tree.heading("Date", text="Date")
        self.forecast_tree.heading("Temperature", text="Temperature (°C)")
        self.forecast_tree.heading("Description", text="Description")
        self.forecast_tree.pack()

    
    def get_api_key(self):
        """Retrieves the API key."""
        with open ("api.txt", "r") as api_key:
            return api_key.read().strip()
    
    def show_weather(self):
        """Retrieves and displays weather information."""
        latitude = self.input_latitude.get().strip()
        longitude = self.input_longitude.get().strip()
        
        if not latitude or not longitude:
            self.weather_info.set("Please enter both the latitude and the longitude.")
            return
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            self.weather_info.set("Invalid latitude or longitude. Please enter numeric values.")
            return

        api_key = self.get_api_key()
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            city = data.get("name", "your selected location")
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            information = (
                f"The current temperature in {city} is {temperature:.1f} degrees Celsius.\n"
                f"Additional details: {description}."
            )
        except Exception as e:
            print(f"Error: {e}")
            information = "Could not retrieve weather data."
        
        self.weather_info.set(information)
        self.show_forecast(latitude, longitude)
    
    def show_forecast(self, latitude, longitude):
        """Retrieves and displays forecast information."""
        api_key = self.get_api_key()
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            forecast_data = response.json()

            # Clear previous forecast data
            for row in self.forecast_tree.get_children():
                self.forecast_tree.delete(row)
            
            daily_forecasts = {}
            today = datetime.now().strftime("%d-%m-%Y")

            # Extract and display forecast data
            for item in forecast_data["list"]:
                date = datetime.fromtimestamp(item["dt"]).strftime("%d-%m-%Y")

                if date == today:
                    continue

                if date not in daily_forecasts:
                    temperature = item["main"]["temp"]
                    description = item["weather"][0]["description"]
                    daily_forecasts[date] = (temperature, description)
                
            for date, (temperature, description) in daily_forecasts.items():
                self.forecast_tree.insert("", "end", values=(date, f"{temperature:.1f}", description))

        except Exception as e:
            print(f"Error: {e}")
            self.weather_info.set(f"{self.weather_info.get()}\nCould not retrieve the forecast.")
    
    def get_coordinates(self):
        """Opens a website to help find coordinates."""
        webbrowser.open("https://latlong.net")

    def quit_app(self):
        """Closes the app."""
        self.master.quit()
    
def main():
    root = tk.Tk()
    Weather(root)
    root.mainloop()

if __name__ == "__main__":
    main()