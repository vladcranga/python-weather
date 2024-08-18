# main.py
from weather.gui import Weather
import tkinter as tk

def main():
    root = tk.Tk()
    Weather(root)
    root.mainloop()

if __name__ == "__main__":
    main()
