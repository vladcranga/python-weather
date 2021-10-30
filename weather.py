"""
weather.py
An app that displays the weather in a location.
It uses the openweathermap API: https: / openweathermap.org/
"""

import PySimpleGUI as sg
import requests
import json
import webbrowser

# the API key
fhand = open(r"api.txt", "r")
api_key = fhand.read()

# specify the theme
sg.theme("BlueMono")

# list the layout elements
left_half = [
    [
        sg.Text("Enter the latitude: "),
        sg.In(size=(25, 1), enable_events=True, key="lat"),
    ],
    [
        sg.Text("Enter the longitude: "),
        sg.In(size=(25, 1), enable_events=True, key="long"),
    ],
    [sg.Button("Show"), sg.Button("Get Coordinates"), sg.Button("Quit")],
]

right_half = [
    [sg.Text("The weather forecast is: ", pad=(145, 0))],
    [sg.Text("", size=(55, 1), key="temperature")],
    [sg.Text("", size=(60, 1), key="temperature_tomorrow")],
]

layout = [[sg.Column(left_half), sg.VSeparator(), sg.Column(right_half)]]

#  create the window
window = sg.Window("Weather Forecast", layout, margins=(10, 10),
                   size=(860, 110))

# the event loop
while True:
    event, values = window.read()

    # display weather information
    if event == "Show":
        lat = values["lat"]
        long = values["long"]

        url = (
            "https://api.openweathermap.org/data/2.5/onecall"
            + "?lat=%s&lon=%s&appid=%s&units=metric" % (lat, long, api_key)
        )

        response = requests.get(url)
        data = json.loads(response.text)

        try:
            temperature = (
                "The current temperature in "
                + data["timezone"]
                + " is "
                + str(data["current"]["temp"])
                + " degrees Celsius."
            )

            temperature_tomorrow = (
                "The temperature tomorrow will be "
                + str(data["daily"][1]["temp"]["day"])
                + " during the day and "
                + str(data["daily"][1]["temp"]["night"])
                + " during the night."
            )

        except Exception:
            temperature = "Could not retrieve weather data."
            temperature_tomorrow = "Could not retrieve future weather data."

        window["temperature"].update(temperature)
        window["temperature_tomorrow"].update(temperature_tomorrow)

    # help the user get coordinates for their location
    if event == "Get Coordinates":
        webbrowser.open("https://latlong.net")

    # close the window
    if event == "Quit" or event == sg.WIN_CLOSED:
        break

window.close()
