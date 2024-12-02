import tkinter as tk
from tkinter import messagebox
import requests

def run():
    pass

def get_coordinates(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None

def get_air_quality(lat, lon, api_key):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        aqi = data['list'][0]['main']['aqi']
        return aqi
    else:
        return None

def check_aqi():
    city_name = city_entry.get()
    api_key = '95a69e951278d464f8127a23c23066c4'

    if city_name:
        lat, lon = get_coordinates(city_name, api_key)
        if lat is not None and lon is not None:
            aqi = get_air_quality(lat, lon, api_key)
            if aqi is not None:
                aqi_desc = {1: 'Good', 2: 'Fair', 3: 'Moderate', 4: 'Poor', 5: 'Very Poor'}
                description = aqi_desc.get(aqi, 'Unknown')

                if aqi == 1:
                    result_label.config(text=f"The AQI for {city_name} is: {description}", fg="white", bg="green")
                elif aqi == 2:
                    result_label.config(text=f"The AQI for {city_name} is: {description}", fg="white", bg="yellowgreen")
                elif aqi == 3:
                    result_label.config(text=f"The AQI for {city_name} is: {description}", fg="black", bg="yellow")
                elif aqi == 4:
                    result_label.config(text=f"The AQI for {city_name} is: {description}", fg="white", bg="orange")
                elif aqi == 5:
                    result_label.config(text=f"The AQI for {city_name} is: {description}", fg="white", bg="red")
            else:
                result_label.config(text="Failed to retrieve AQI data.", fg="white", bg="red")
        else:
            result_label.config(text="City not found or invalid.", fg="white", bg="red")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

window = tk.Tk()
window.title("Air Quality Index Checker")
window.geometry("500x400")
window.configure(bg="#f0f0f0")

city_label = tk.Label(window, text="Enter City Name:", font=("Arial", 16), bg="#f0f0f0", fg="black")
city_label.pack(pady=20)

city_entry = tk.Entry(window, width=40, font=("Arial", 14))
city_entry.pack(pady=10)

check_button = tk.Button(window, text="Check AQI", command=check_aqi, font=("Arial", 14), bg="#4CAF50", fg="white", width=15, height=2, relief="raised")
check_button.pack(pady=20)

result_label = tk.Label(window, text="", font=("Arial", 18), bg="#f0f0f0", fg="black", width=30, height=3, relief="solid")
result_label.pack(pady=20)

window.mainloop()
