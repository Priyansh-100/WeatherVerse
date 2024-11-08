WeatherVerse

# Weather Data Fetching Tool with City Name Lookup

This Python application allows you to fetch and display weather data for a specified city or coordinates using the Open-Meteo API.
The tool includes a Tkinter-based GUI for user input, allowing you to either enter the city name or coordinates to retrieve weather data.
It also includes functionality to convert a city name into its corresponding latitude and longitude.

## Features

- Fetch current weather data: temperature, humidity, precipitation, and rain information.
- Retrieve hourly weather data: temperature, humidity, precipitation probability, and visibility.
- Fetch daily weather data: weather code for daily conditions.
- City Name Lookup: Convert a city name into latitude and longitude coordinates.
- Caching: The application uses `requests_cache` to cache API responses for faster subsequent requests.
- Retry Mechanism: Automatically retries the request up to 5 times in case of failure, with an exponential backoff.
- Outputs the weather data as pandas DataFrames for easy manipulation and visualization.

## Requirements

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- `openmeteo_requests`: Client for the Open-Meteo API.
- `requests_cache`: For caching API responses.
- `retry_requests`: To automatically retry failed API requests.
- `pandas`: To process and display weather data.
- `geopy`: For converting city names to coordinates (latitude and longitude).
- `tkinter`: For the GUI.

You can install the required libraries using `pip`:

```bash
pip install openmeteo_requests requests_cache retry_requests pandas geopy
