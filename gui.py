"""
    Engineering 498
    Let's Boil a Computer
    Rusty Rinehart
    Chris Bremser
    Jesus Arias
    Prasanna Raut
    Sean Brown
"""
from cProfile import label
import math
from pydoc import tempfilepager
from tkinter import TOP, Canvas, Label, Tk, ttk
from PIL import Image, ImageTk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (NavigationToolbar2Tk, FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import numpy as np
import time


class GUI:
    """
        This class holds all GUI information
    """

    def __init__(self, master):
        self.master = master

        # Attributes
        self.temperature = None
        self.pressure = None

        self.master.title("Let's Boil a Computer Again")

        self.gui_outline()

    def gui_outline(self):
        self.top_bar_frame = ttk.Frame(self.master)
        self.middle_bar_frame = ttk.Frame(self.master)
        self.bottom_bar_frame = ttk.Frame(self.master)
        self.top_bar_frame.pack()
        self.middle_bar_frame.pack()
        self.bottom_bar_frame.pack()
        self.top_bar()
        self.middle_bar()
        self.bottom_bar()

    def top_bar(self):
        self.fluid_level_frame = ttk.Frame(self.top_bar_frame)
        fluid_level_label = ttk.Label(
            self.fluid_level_frame, text="Fluid Level: ")
        self.fluid_level_value = ttk.Label(self.fluid_level_frame, text="NULL")
        fluid_level_label.pack()
        self.fluid_level_value.pack()
        self.fluid_level_frame.pack(side="left")

        self.title_bar = ttk.Frame(self.top_bar_frame)
        image = Image.open("koolance.jpg").resize((172, 49))
        self.koolance_image = ImageTk.PhotoImage(image)
        self.koolance_label = ttk.Label(self.title_bar, text="Koolance")
        self.koolance_image_label = ttk.Label(
            self.title_bar, image=self.koolance_image)
        self.koolance_label.pack(side="left")
        self.koolance_image_label.pack(side="left")
        self.title_bar.pack(side="left")

        self.settings_frame = ttk.Frame(self.top_bar_frame)
        image = Image.open("settings.png").resize((64, 64))
        self.settings_image = ImageTk.PhotoImage(image)
        self.settings_image_label = ttk.Button(
            self.settings_frame, image=self.settings_image)
        self.settings_image_label.pack()
        self.settings_frame.pack(side="left")

    def middle_bar(self):
        self.graph_frame = ttk.Frame(self.middle_bar_frame)
        self.draw_graph()
        self.graph_frame.pack(side = "top")


    def bottom_bar(self):
        self.pump_pressure_frame = ttk.Frame(self.bottom_bar_frame)
        self.temp_frame = ttk.Frame(self.bottom_bar_frame)
        self.draw_pump_guage()
        self.draw_thermometer()
        self.pump_pressure_frame.pack(side="left")
        self.temp_frame.pack(side="left")

    def draw_graph(self):
        self.graph_figure = Figure(figsize=(7, 4), dpi=100)
        self.temperature_plot = self.graph_figure.add_subplot(111)
        self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master=self.middle_bar_frame)
        self.graph_canvas.draw()
        self.pressure_plot = self.temperature_plot.twinx()
        self.xtime = []
        self.pressure = []
        self.temperature = []
        self.pressure_plot.plot(self.xtime, self.pressure, color = "red", label = 'pressure')
        self.temperature_plot.plot(self.xtime, self.temperature, color = "blue", label = 'temperature')
        self.graph_figure.legend(loc = 'upper center')
        self.graph_canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas)
        self.toolbar.update()
        self.graph_canvas.get_tk_widget().pack()

    def set_graph(self, newPressure, newTemperature, newTime):
        self.xtime = self.xtime[-20:]
        self.pressure = self.pressure[-20:]
        self.temperature = self.temperature[-20:]

        self.temperature.append(newTemperature)
        self.pressure.append(newPressure)
        self.xtime.append(newTime)
        
        self.pressure_plot.plot(self.xtime, self.pressure, color = "red")
        self.temperature_plot.plot(self.xtime, self.temperature, color = "blue")
        self.temperature_plot.set_xlim(self.xtime[0],self.xtime[-1], 1)

        self.pressure_plot.set_ylabel("Temperature (°C)")
        self.temperature_plot.set_ylabel("Pressure (Psi)")
        self.temperature_plot.set_xlabel("Time (s)")

        self.graph_canvas.draw()
        self.graph_canvas.flush_events()
        print(self.temperature)
        print(self.pressure)
        print(self.xtime)
        time.sleep(0.05)

    def draw_pump_guage(self):
        press_label_frame = ttk.Frame(self.pump_pressure_frame)
        press_label_frame.pack()
        press_label = ttk.Label(press_label_frame, text="Pressure:")
        press_label.pack(side="left")
        self.press_value = ttk.Label(press_label_frame, text="NULL")
        self.press_value.pack(side="left")
        self.press_canvas = Canvas(
            self.pump_pressure_frame, width=100, height=100)
        # Create barometer
        self.press_canvas.create_oval(25, 25, 75, 75, width=10, outline="gray")
        self.press_canvas.create_arc(25, 25, 75, 75, start=135,
                                     extent=90, fill="green", width=0, outline="green")
        self.press_canvas.create_arc(25, 25, 75, 75, start=45,
                                     extent=90, fill="yellow", width=0, outline="yellow")
        self.press_canvas.create_arc(25, 25, 75, 75, start=315,
                                     extent=90, fill="red", width=0, outline="red")
        self.press_canvas.create_arc(25, 25, 75, 75, start=225,
                                     extent=90, fill="#d8d8d8", width=0, outline="#d8d8d8")
        self.press_canvas.pack()
        self.press_canvas.create_oval(40, 40, 60, 60, width=10,
                                      outline="#d8d8d8", fill="#d8d8d8")
        self.press_canvas.create_rectangle(
            45, 80, 55, 90, fill="gray", outline="gray")
        # Create needle
        needle_endpoint = self.needle_coords(225)
        self.needle = self.press_canvas.create_line(
            50, 50, needle_endpoint[0], needle_endpoint[1], fill="blue", width=3)
        self.press_canvas.create_oval(45, 45, 55, 55, fill="blue", width=0)

    def set_pump_pressure(self, new_press):
        """Sets the pressure and animates barometer accordingly"""
        self.pressure = new_press
        self.press_value.config(text=new_press)
        new_press = abs(new_press)
        if new_press > 3:
            new_press = 3
        theta = 225 - (new_press / 3) * 270
        needle_endpoint = self.needle_coords(theta)
        self.press_canvas.coords(
            self.needle, 50, 50, needle_endpoint[0], needle_endpoint[1])

    def draw_thermometer(self):
        temp_label = ttk.Label(self.temp_frame, text="Temperature:")
        temp_label.pack()
        self.temp_value = ttk.Label(self.temp_frame, text="NULL")
        self.temp_value.pack()
        self.therm_canvas = Canvas(self.temp_frame, width=100, height=100)
        self.therm_canvas.create_rectangle(
            40, 10, 60, 80, fill="white", width=0)
        self.therm_circ = self.therm_canvas.create_oval(
            35, 70, 65, 100, fill="black", width=0)
        # Create rectangle that will change size
        self.therm_rect = self.therm_canvas.create_rectangle(
            40, 70, 60, 80, fill="black", width=0)
        self.therm_canvas.pack()

    def set_temperature(self, new_temp):
        """Sets the temperature and adjusts thermometer animation accordingly"""
        self.temperature = new_temp
        # Temperatures only visually supported between 20 and 60
        if new_temp < 20:
            new_temp = 20
        if new_temp > 60:
            new_temp = 60
        # Adjust temperature value on GUI
        self.temp_value.config(text=self.temperature)
        # Calculate height needed by rectangle to simulate where thermometer is
        height = (new_temp - 20) * 1.5
        # Update rectangle coordinates to change height
        self.therm_canvas.coords(self.therm_rect, 40, 70 - height, 60, 80)
        # Get a scaled color shift value based on temperature
        # Get red value in hex
        color_shift = int(((new_temp - 20) / 40.0) * 255)
        red = hex(color_shift)[2:]
        # If statement needed to give leading zero to single digit hex value
        if len(red) == 1:
            red = "0" + red
        # Green value won't change
        green = "00"
        # Get blue value in hex
        blue = hex(255 - color_shift)[2:]
        # If statement needed to give leading zero to single digit hex value
        if len(blue) == 1:
            blue = "0" + blue
        # Generate hex color
        new_color = f"#{red}{green}{blue}"
        print(new_color)
        print(f"Red = {color_shift}, Blue = {255 - color_shift}")
        # Update color
        self.therm_canvas.itemconfig(self.therm_rect, fill=new_color)
        self.therm_canvas.itemconfig(self.therm_circ, fill=new_color)

    def needle_coords(self, theta):
        """Given an angle (degrees), calculates coordinates of endpoint of line of needle"""
        # Needle length
        needle_length = 20
        alpha = math.radians(theta - 180)
        delta_x = needle_length * math.cos(alpha)
        delta_y = needle_length * math.sin(alpha)
        return (50 - delta_x, 50 + delta_y)


def main():
    root = Tk()
    gui = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()