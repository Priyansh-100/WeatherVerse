import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import colorchooser
from tkinter.simpledialog import askstring

if __name__ == "__main__":
    import Login
    Login.run()

def run():
    pass

def open_weather_app():
    root.destroy()
    import Specific
    Specific.run()

def show_about():
    root.destroy()
    import About
    About.run()

def open_settings():
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        root.config(bg=color_code)

def run():
    global root
    root = tk.Tk()
    root.title("Weather Application")
    root.geometry("800x600")
    root.resizable(True, True)

    bg_image_path = "D:/download.jpg"
    try:
        bg_image = Image.open(bg_image_path)
        bg_image = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load background image: {e}")
        bg_image = None

    if bg_image:
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(root, text="Welcome to the Weather App", font=("Helvetica", 24, "bold"), fg="white", pady=20,
                           bg="#000000", relief="solid")
    title_label.pack(fill="x", pady=20)

    settings_button = tk.Button(root, text="Settings", font=("Helvetica", 14), command=open_settings, bg="#4CAF50",
                                fg="white", relief="raised", bd=5)
    settings_button.place(x=710, y=20)

    weather_button = tk.Button(root, text="Check Weather", font=("Helvetica", 18), width=20, height=2,
                               command=open_weather_app, bg="#4CAF50", fg="white", relief="raised", bd=5)
    weather_button.pack(pady=20)

    about_button = tk.Button(root, text="About", font=("Helvetica", 18), width=20, height=2, command=show_about,
                             bg="#008CBA", fg="white", relief="raised", bd=5)
    about_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", font=("Helvetica", 18), width=20, height=2, command=root.quit,
                            bg="#f44336", fg="white", relief="raised", bd=5)
    exit_button.pack(pady=40)

    root.mainloop()
