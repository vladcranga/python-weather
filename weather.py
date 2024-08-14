# weather.py
# An app that displays the weather in a location.
# It uses the openweathermap API: https: / openweathermap.org/


import PySimpleGUI as sg
import requests
import json
import webbrowser

# the API key
fhand = open("api.txt", "r")
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
    [sg.Text("Weather Information: ", pad=(145, 0))],
    [sg.Text("", size=(70, 2), key="weather_info")],
]

layout = [[sg.Column(left_half), sg.VSeparator(), sg.Column(right_half)]]

#  create the window
window = sg.Window("Weather Forecast", layout, margins=(10, 10),
                   size=(860, 130))

# the event loop
while True:
    event, values = window.read()

    # display weather information
    if event == "Show":
        lat = values["lat"]
        long = values["long"]
        
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = json.loads(response.text)

        try:
            city = data.get("name", "your chosen location")
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            information = (
                f"The current temperature in {city} is {temperature:.1f} degrees Celsius.\n"
                f"Additional details: {description}."
            )

        except Exception:
            information = "Could not retrieve weather data."

        window["weather_info"].update(information)

    # help the user get coordinates for their location
    if event == "Get Coordinates":
        webbrowser.open("https://latlong.net")

    # close the window
    if event == "Quit" or event == sg.WIN_CLOSED:
        break

window.close()
