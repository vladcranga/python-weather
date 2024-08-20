# main.py
from weather.gui import Weather
import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    Weather(root)

    # Weather icons created by iconixar - Flaticon
    # https://www.flaticon.com/free-icons/weather
    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(True, icon)
    
    root.mainloop()

if __name__ == "__main__":
    main()
