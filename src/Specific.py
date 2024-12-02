import tkinter as tk
from tkinter import messagebox

# Function to be implemented for AQI functionality
def show_air_quality():
    import AirQualityIndex
    AirQualityIndex.run()

def run():
    pass

def return_():
    root.destroy()
    Main()

def Main():
    import Main
    Main.run()

def show_simple_weather():
    import GuiWeather
    GuiWeather.run()

def show_specific_weather():
    import fetchData
    fetchData.run()

# Create the main window
root = tk.Tk()
root.title("Weather Data Format")
root.geometry("500x400")  # Increased window size to accommodate new button
root.configure(bg="#ADD8E6")

# Create a label for the title
label = tk.Label(root, text="Choose Weather Data Type", font=("Arial", 16), bg="#ADD8E6")
label.pack(pady=30)

# Create buttons for user selection
simple_weather_button = tk.Button(root, text="Simple Weather Data", font=("Arial", 12), command=show_simple_weather)
simple_weather_button.pack(pady=15)

specific_weather_button = tk.Button(root, text="Specific Weather Data", font=("Arial", 12), command=show_specific_weather)
specific_weather_button.pack(pady=15)

# New button for Air Quality Index
air_quality_button = tk.Button(root, text="Air Quality Index", font=("Arial", 12), command=show_air_quality)
air_quality_button.pack(pady=15)

# Return button
return_button = tk.Button(root, text="Return", command=return_)
return_button.pack(pady=20)

# Exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

# Run the application
root.mainloop()
