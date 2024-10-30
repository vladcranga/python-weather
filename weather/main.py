from weather.gui import Weather
from weather.data import get_file_path
import tkinter as tk

def main():
    """Initialises the main window and starts the Tkinter main event loop."""
    root = tk.Tk()
    Weather(root)

    # Weather icons created by iconixar - Flaticon
    # https://www.flaticon.com/free-icons/weather
    icon_path = get_file_path("icon.png")
    try:
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
    except Exception as e:
        print(f"Error loading icon: {e}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
