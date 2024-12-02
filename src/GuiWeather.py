import tkinter as tk
from tkinter import messagebox
import requests
import json
import geocoder

API_KEY = "4598b220418b4103a022758ffbb725fb"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q="

def run():
    pass

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 781:
        return "🌫️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "🌤️"
    else:
        return "🌈"

def get_weather_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None

def parse_and_display_weather(json_response):
    try:
        data = json.loads(json_response)
        city_name = data.get("name", "N/A")

        main = data.get("main", {})
        temperature = main.get("temp", "N/A")
        feels_like = main.get("feels_like", "N/A")
        humidity = main.get("humidity", "N/A")

        weather_array = data.get("weather", [])
        weather_description = weather_array[0].get("description", "N/A") if weather_array else "N/A"
        weather_id = weather_array[0].get("id", -1) if weather_array else -1

        weather_emoji = get_weather_emoji(weather_id)

        result_text = f"Weather in {city_name} {weather_emoji}:\n"
        result_text += f"Temperature: {temperature if temperature != 'N/A' else 'N/A'}°C\n"
        result_text += f"Feels Like: {feels_like if feels_like != 'N/A' else 'N/A'}°C\n"
        result_text += f"Humidity: {humidity if humidity != 'N/A' else 'N/A'}%\n"
        result_text += f"Description: {weather_description}"

        weather_result_label.config(text=result_text)
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Error parsing weather data: {e}")

def on_get_weather():
    city = city_entry.get().strip()
    if city:
        url = f"{BASE_URL}{city}&appid={API_KEY}&units=metric"
    else:
        city = get_location()
        if not city:
            messagebox.showwarning("Input Error", "Unable to detect location.")
            return
        url = f"{BASE_URL}{city}&appid={API_KEY}&units=metric"

    response = get_weather_data(url)
    if response:
        parse_and_display_weather(response)

def get_location():
    g = geocoder.ip('me')
    return g.city

root = tk.Tk()
root.title("Weather App")
root.configure(bg='#e6d1f7')

tk.Label(root, bg='#e6d1f7', text="Enter city name :").pack(pady=10)

city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

get_weather_button = tk.Button(root, text="Get Weather", command=on_get_weather)
get_weather_button.pack(pady=10)

weather_result_label = tk.Label(root, text="", font=("Helvetica", 14), width=40, height=8, relief="solid", anchor="w", justify="left", bg='#ffffff')
weather_result_label.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()
