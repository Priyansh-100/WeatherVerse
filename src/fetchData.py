import tkinter as tk
from tkinter import ttk, messagebox
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def run():
    pass

from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def export_pdf():
    try:
        if not hourly_treeview.get_children() and not daily_treeview.get_children():
            raise ValueError("No data available to export.")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Weather Data as PDF"
        )

        if not file_path:
            return

        pdf = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, height - 40, "Weather Data Report")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(30, height - 80, "Hourly Weather Data:")

        y_position = height - 100
        for child in hourly_treeview.get_children():
            time, temp, humidity = hourly_treeview.item(child, "values")
            y_position -= 20
            pdf.setFont("Helvetica", 10)
            pdf.drawString(30, y_position, f"{time} - Temp: {temp} - Humidity: {humidity}")
            if y_position < 60:
                pdf.showPage()
                y_position = height - 40

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(30, y_position - 20, "Daily Weather Data:")

        y_position -= 40
        for child in daily_treeview.get_children():
            date, max_temp, min_temp = daily_treeview.item(child, "values")
            y_position -= 20
            pdf.setFont("Helvetica", 10)
            pdf.drawString(30, y_position, f"{date} - Max Temp: {max_temp} - Min Temp: {min_temp}")
            if y_position < 60:
                pdf.showPage()
                y_position = height - 40

        pdf.save()

        messagebox.showinfo("Export Successful", f"Weather data has been successfully exported to {file_path}")

    except ValueError as ve:
        messagebox.showerror("No Data", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data to PDF:\n{e}")

def get_coordinates(city_name):
    api_key = "95a69e951278d464f8127a23c23066c4"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to connect to API.")
    data = response.json()
    if not data:
        raise Exception("City not found.")
    latitude = data[0]['lat']
    longitude = data[0]['lon']
    return latitude, longitude

def on_get_coordinates():
    city_name = city_entry.get().strip()
    if not city_name:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    try:
        latitude, longitude = get_coordinates(city_name)
        latitude_entry.delete(0, tk.END)
        latitude_entry.insert(0, str(latitude))
        longitude_entry.delete(0, tk.END)
        longitude_entry.insert(0, str(longitude))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get coordinates: {str(e)}")

def fetch_weather():
    current_label.config(text="Current Weather:\n")
    clear_treeview(hourly_treeview)
    clear_treeview(daily_treeview)

    latitude = latitude_entry.get().strip()
    longitude = longitude_entry.get().strip()

    if not latitude or not longitude:
        messagebox.showerror("Input Error", "Please enter both latitude and longitude or city name.")
        return

    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "weather_code"],
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "precipitation", "visibility"],
            "daily": ["temperature_2m_max", "temperature_2m_min"],
            "timezone": "auto"
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        current = response.Current()
        current_temperature = current.Variables(0).Value()
        current_humidity = current.Variables(1).Value()
        current_precipitation = current.Variables(2).Value()

        current_label.config(
            text=f"Current Weather:\n"
                 f"Temperature: {current_temperature:.2f}°C\n"
                 f"Humidity: {current_humidity:.2f}%\n"
                 f"Precipitation: {current_precipitation:.2f} mm"
        )

        if current_temperature < 10:
            root.config(bg='lightblue')
        elif current_temperature < 20:
            root.config(bg='lightgreen')
        else:
            root.config(bg='lightyellow')

        hourly = response.Hourly()
        hourly_time = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
        hourly_temperature = hourly.Variables(0).ValuesAsNumpy()
        hourly_humidity = hourly.Variables(1).ValuesAsNumpy()

        for hour, temp, humidity in zip(hourly_time[:24], hourly_temperature[:24], hourly_humidity[:24]):
            hourly_treeview.insert("", "end", values=(hour.strftime('%Y-%m-%d %H:%M'), f"{temp:.2f}°C", f"{humidity:.2f}%"))

        daily = response.Daily()
        daily_time = pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )
        daily_temperature_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_min = daily.Variables(1).ValuesAsNumpy()

        for day, max_temp, min_temp in zip(daily_time[:3], daily_temperature_max[:3], daily_temperature_min[:3]):
            daily_treeview.insert("", "end", values=(day.strftime('%Y-%m-%d'), f"{max_temp:.2f}°C", f"{min_temp:.2f}°C"))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data:\n{e}")

def clear_treeview(treeview):
    for item in treeview.get_children():
        treeview.delete(item)

root = tk.Tk()
root.title("Specific Weather App")
root.geometry("600x800")

root.config(bg='lightblue')

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x", padx=10, pady=10)

ttk.Label(frame, text="City Name:").grid(row=0, column=0, sticky="w")
city_entry = ttk.Entry(frame, width=20)
city_entry.grid(row=0, column=1, sticky="w")

ttk.Label(frame, text="Latitude:").grid(row=1, column=0, sticky="w")
latitude_entry = ttk.Entry(frame, width=20)
latitude_entry.grid(row=1, column=1, sticky="w")

ttk.Label(frame, text="Longitude:").grid(row=2, column=0, sticky="w")
longitude_entry = ttk.Entry(frame, width=20)
longitude_entry.grid(row=2, column=1, sticky="w")

get_coordinates_button = ttk.Button(frame, text="Get Coordinates", command=on_get_coordinates)
get_coordinates_button.grid(row=3, column=0, columnspan=2, pady=10)

fetch_button = ttk.Button(frame, text="Fetch Weather", command=fetch_weather)
fetch_button.grid(row=4, column=0, columnspan=2, pady=10)

export_button = ttk.Button(frame, text="Export PDF", command=export_pdf)
export_button.grid(row=5, column=0, columnspan=2, pady=10)

current_label = ttk.Label(root, text="Current Weather:\n", padding=10)
current_label.pack(fill="x", padx=10, pady=10)

hourly_frame = ttk.Frame(root, padding=10)
hourly_frame.pack(fill="x", padx=10, pady=10)

ttk.Label(hourly_frame, text="Hourly Weather:").pack()
hourly_treeview = ttk.Treeview(hourly_frame, columns=("Time", "Temperature", "Humidity"), show="headings")
hourly_treeview.heading("Time", text="Time")
hourly_treeview.heading("Temperature", text="Temperature")
hourly_treeview.heading("Humidity", text="Humidity")
hourly_treeview.pack(fill="both", expand=True)

daily_frame = ttk.Frame(root, padding=10)
daily_frame.pack(fill="x", padx=10, pady=10)

ttk.Label(daily_frame, text="Daily Weather:").pack()
daily_treeview = ttk.Treeview(daily_frame, columns=("Date", "Max Temp", "Min Temp"), show="headings")
daily_treeview.heading("Date", text="Date")
daily_treeview.heading("Max Temp", text="Max Temp")
daily_treeview.heading("Min Temp", text="Min Temp")
daily_treeview.pack(fill="both", expand=True)

root.grid_rowconfigure(0, weight=1, minsize=50)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
