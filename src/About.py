import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("About WeatherVerse")
root.geometry("800x550")


root.configure(bg='#a8d0e6')

def run():
    pass

def close_app():
    root.destroy()

def return_to_previous():
    root.destroy()
    Main()

def Main():
    import Main
    Main.run()

# Add a title label
title_label = tk.Label(
    root,
    text="About WeatherVerse",
    font=("Helvetica", 18, "bold"),
    pady=10,
    bg='#a8d0e6'
)
title_label.pack()

# Add description text
about_text = (
    "Welcome to WeatherVerse, your trusted companion for accurate and up-to-date weather information!\n\n"
    "Our mission is to simplify how you interact with weather data by providing a seamless, user-friendly experience. "
    "Whether you're planning your day, preparing for a trip, or just curious about the weather around the globe, "
    "WeatherVerse is here to keep you informed.\n\n"
    "Features You’ll Love:\n"
    "- Real-Time Weather Updates\n"
    "- Interactive App\n"
    "- Custom Alerts\n"
    "- Global Reach\n\n"
    "Why Choose WeatherVerse?\n"
    "WeatherVerse combines advanced meteorological data with intuitive design to ensure that you always have the "
    "most reliable information at your fingertips.\n\n"
    "Stay connected with us:\n"
    "Email: support@weatherverse.com\n"
    "Website: www.weatherverse.com"
)
about_label = tk.Label(
    root,
    text=about_text,
    font=("Helvetica", 12),
    justify="left",
    wraplength=550,
    bg='#a8d0e6'
)
about_label.pack(pady=10)

return_button = ttk.Button(root, text ="Return", command = return_to_previous)
return_button.pack(pady=10)

# Add a close button
close_button = ttk.Button(root, text="Close", command=close_app)
close_button.pack(pady=10)

# Run the main event loop
root.mainloop()
