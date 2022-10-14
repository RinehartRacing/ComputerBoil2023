"""
    Engineering 498
    Let's Boil a Computer
    Rusty Rinehart
    Chris Bremser
    Jesus Arias
    Prasanna Raut
    Sean Brown
"""
import math
from tkinter import Canvas, Tk, ttk
from PIL import Image, ImageTk
from gui import GUI
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import numpy as np  


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
        self.graph_figure = Figure(figsize = (5,1), dpi = 100)
        self.x = np.linspace(0, 10*np.pi, 100)
        self.y = np.sin(self.x)
        self.graph_plot = self.graph_figure.add_subplot(111)
        self.graph_plot.plot(self.y)
        self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master = self.middle_bar_frame)
        self.graph_canvas.draw()

        self.graph_canvas.get_tk_widget().pack() #.grid(row = 0, column = 1, rowspan= 1, columnspan= 2)

    def bottom_bar(self):
        self.pump_pressure_frame = ttk.Frame(self.bottom_bar_frame)
        self.draw_pump_guage()
        self.pump_pressure_frame.pack(side="left")

    def draw_pump_guage(self):
        press_label_frame = ttk.Frame(self.pump_pressure_frame)
        press_label_frame.pack()
        press_label = ttk.Label(press_label_frame, text="Pressure:")
        press_label.pack(side="left")
        self.press_value = ttk.Label(press_label_frame, text="NULL")
        self.press_value.pack(side="left")
        self.press_canvas = Canvas(self.pump_pressure_frame, width=100, height=100)
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
