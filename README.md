# Python Weather App

This is a weather app made using Python and the [openweathermap](https://openweathermap.org) API.

## Requirements
- Python 3
- requests
- A free API key from [openweathermap](https://openweathermap.org)

```
pip install -r requirements.txt
```

## How to run the application
Enter 
```
python -m weather.main
```
in the **python-weather** directory.

- Your API key should be in *config.json* in the python-weather directory:
```
{
    "api_key": "your_api_key"
}
```

## Features:
- Displays the current temperature and a five-day forecast for a location based on coordinates or city
- Has a button which opens a location-to-coordinates website
- Add cities to favourites

![example picture](example.png)

## Credits

- GUI Icon: Weather icon by iconixar from [Flaticon](https://www.flaticon.com/free-icons/weather).
