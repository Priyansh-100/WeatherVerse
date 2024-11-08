import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Assuming fetch_weather_data is defined as per the previous code snippet

def display_weather_data():
    try:
        # Retrieve user input for coordinates
        latitude = float(latitude_entry.get())
        longitude = float(longitude_entry.get())

        # Fetch weather data using the function
        weather_data = fetch_weather_data(latitude, longitude)

        # Display current data
        current_data_text.delete("1.0", tk.END)
        current_data_text.insert(tk.END, f"Current Data:\n")
        for key, value in weather_data["current"].items():
            current_data_text.insert(tk.END, f"{key}: {value}\n")

        # Display hourly data
        hourly_data_text.delete("1.0", tk.END)
        hourly_data_text.insert(tk.END, f"Hourly Data:\n{weather_data['hourly'].head()}\n")

        # Display daily data
        daily_data_text.delete("1.0", tk.END)
        daily_data_text.insert(tk.END, f"Daily Data:\n{weather_data['daily'].head()}\n")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Weather Data Viewer")
root.geometry("600x700")

# Title label
title_label = ttk.Label(root, text="Weather Data Viewer", font=("Arial", 16))
title_label.pack(pady=10)

# Latitude and Longitude input frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Latitude entry
latitude_label = ttk.Label(input_frame, text="Latitude:")
latitude_label.grid(row=0, column=0, padx=5, pady=5)
latitude_entry = ttk.Entry(input_frame, width=20)
latitude_entry.grid(row=0, column=1, padx=5, pady=5)

# Longitude entry
longitude_label = ttk.Label(input_frame, text="Longitude:")
longitude_label.grid(row=1, column=0, padx=5, pady=5)
longitude_entry = ttk.Entry(input_frame, width=20)
longitude_entry.grid(row=1, column=1, padx=5, pady=5)

# Fetch Data button
fetch_button = ttk.Button(root, text="Fetch Weather Data", command=display_weather_data)
fetch_button.pack(pady=10)

# Text widget to display current data
current_data_label = ttk.Label(root, text="Current Weather Data:")
current_data_label.pack()
current_data_text = tk.Text(root, height=10, width=60, wrap=tk.WORD)
current_data_text.pack(pady=5)

# Text widget to display hourly data
hourly_data_label = ttk.Label(root, text="Hourly Weather Data:")
hourly_data_label.pack()
hourly_data_text = tk.Text(root, height=10, width=60, wrap=tk.WORD)
hourly_data_text.pack(pady=5)

# Text widget to display daily data
daily_data_label = ttk.Label(root, text="Daily Weather Data:")
daily_data_label.pack()
daily_data_text = tk.Text(root, height=10, width=60, wrap=tk.WORD)
daily_data_text.pack(pady=5)

# Run the application
root.mainloop()
