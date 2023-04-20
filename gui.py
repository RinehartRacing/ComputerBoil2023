"""
    Engineering 498
    Let's Boil a Computer
    Rusty Rinehart
    Chris Bremser
    Jesus Arias
    Prasanna Raut
    Sean Brown
"""
#Dark Mode Hex Colors
#18191a background black
#242526 card medium black/grey
#3a3b3c hover card dark grey
#e4e6eb primary text white
#bob3b8 secondary text light grey

from cProfile import label
import math
from pydoc import tempfilepager
from tkinter import Canvas, Tk, ttk, Button, Frame, Toplevel
from PIL import Image, ImageTk
from settings import Settings

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (NavigationToolbar2Tk, FigureCanvasTkAgg)
import matplotlib.pyplot as plt
import numpy as np

class VerticalNavigationToolbar2Tk(NavigationToolbar2Tk):
        def __init__(self, canvas, window):
            super().__init__(canvas, window, pack_toolbar=True)

        # override _Button() to re-pack the toolbar button in vertical direction
        def _Button(self, text, image_file, toggle, command):
            b = super()._Button(text, image_file, toggle, command)
            b.pack(side="top") # re-pack button in vertical direction
            return b

        # override _Spacer() to create vertical separator
        def _Spacer(self):
            s = ttk.Frame(self, width=30, relief= "sunken", padding=20)
            s.pack(side="top", pady=10, padx=5) # pack in vertical direction
            return s

        # disable showing mouse position in toolbar
        def set_message(self, s):
            pass

class GUI:
    """
        This class holds all GUI information
    """

    def __init__(self, master, control):
        self.master = master
        self.control = control
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
        self.middle_bar_frame.pack(fill="x")
        self.bottom_bar_frame.pack()
        self.top_bar()
        self.middle_bar()
        self.bottom_bar()
        #Colors foreground="#e4e6eb", background="#242526"
        # Set GUI to darkmode
        style = ttk.Style() 
        self.master.configure(bg="#18191A")
        style.configure("TLabel", foreground="#e4e6eb", background="#18191A")
        style.configure("TFrame", background="#18191A", foreground="blue" )
        style.configure("TButton", padding =-1)

    def top_bar(self):
        self.draw_filter()
        self.draw_fluid_level()
        self.draw_koolance()
        self.draw_settings()
        

    def middle_bar(self):
        self.graph_frame = ttk.Frame(self.middle_bar_frame)
        self.draw_graph()
        self.graph_frame.pack(side = "top")

    def bottom_bar(self):
        self.flow_rate_frame = ttk.Frame(self.bottom_bar_frame)
        self.pump_pressure_frame = ttk.Frame(self.bottom_bar_frame)
        self.temp_frame = ttk.Frame(self.bottom_bar_frame)
        
        self.draw_flow_rate()
        self.draw_pump_gauge()
        self.draw_thermometer()

        self.flow_rate_frame.pack(side="left", fill = "both")
        self.pump_pressure_frame.pack(side="left", fill="both")
        self.temp_frame.pack(side="left", fill="both")

    def draw_filter(self):
        self.filter_frame = Frame(self.top_bar_frame)
        image = Image.open("filter.png").resize((64, 64))
        self.filter_image = ImageTk.PhotoImage(image)
        self.filter_image_label = Button(
            self.filter_frame, command=self.toggle_pump, image = self.filter_image, borderwidth= 0, highlightthickness=0, background= "#18191A", foreground= "#18191A")
        #     ##Above fix the image, apparently its about the borderwidth and height thickness or something. figure out the method
        #     #for a ttk button
        self.filter_image_label.pack()
        self.filter_frame.pack(side="left")

    def toggle_pump(self):
        print("Toggling pump")
        self.control.toggle_override()
        self.control.toggle_pump()

    def apply_settings(self, time_start, time_duration):
        self.control.apply_settings(time_start, time_duration)
    def draw_koolance(self):
        self.title_bar = ttk.Frame(self.top_bar_frame)
        image = Image.open("koolance-off.png").resize((172, 49))
        self.koolance_image = ImageTk.PhotoImage(image)
        self.koolance_label = ttk.Label(self.title_bar)
        self.koolance_image_label = ttk.Label(
            self.title_bar, image=self.koolance_image)
        self.koolance_label.pack(side="left")
        self.koolance_image_label.pack(side="left")
        self.title_bar.pack(side="left")

    def draw_settings(self):
        self.settings_frame = Frame(self.top_bar_frame)
        image = Image.open("settings.png").resize((64, 64))
        self.settings_image = ImageTk.PhotoImage(image)
        self.settings_image_label = Button(
            self.settings_frame, command=self.open_popup, image = self.settings_image, borderwidth= 0, highlightthickness=0, background= "#18191A", foreground= "#18191A")
        #     ##Above fix the image, apparently its about the borderwidth and height thickness or something. figure out the method
        #     #for a ttk button
        self.settings_image_label.pack()
        self.settings_frame.pack(side="left")
    
    def open_popup(self):
       
       top = Toplevel()
       self.settings = Settings(top, self)
       top.geometry("750x250")
       popup_label = ttk.Label()
       
    def draw_fluid_level(self):
        self.fluid_level_frame = ttk.Frame(self.top_bar_frame)
        fluid_level_label = ttk.Label(
            self.fluid_level_frame, text="Fluid Level: ")
        self.fluid_level_value = ttk.Label(self.fluid_level_frame, text="NULL")
        fluid_level_label.pack()
        self.fluid_level_value.pack()
        self.fluid_level_frame.pack(side="left")

    def draw_graph(self):
        with plt.rc_context({'axes.edgecolor':'#B0B3B8'}):
            ##Creates a figure of size 700 by 470
            self.graph_figure = Figure(figsize=(7, 4.7), dpi=100)
            ##Creates a plot for temperature by adding the plot as a subplot to the figure
            self.temperature_plot = self.graph_figure.add_subplot(111)
            #Adds the figure to the middle bar frame of the tkInter window.
            self.graph_canvas = FigureCanvasTkAgg(self.graph_figure, master=self.middle_bar_frame)
            self.graph_canvas.draw()
            #create toolbar frame
            self.toolbar_frame = ttk.Frame(self.middle_bar_frame)
            #creates the vertical navigationtoolbar2tk
            self.toolbar = VerticalNavigationToolbar2Tk(self.graph_canvas, self.toolbar_frame)
            self.toolbar.update()
            self.toolbar.pack(side="left", fill="both")
            self.toolbar_frame.pack(side="left", fill="y")
            ##Creates a twin axis for the temperature and pressure plots so they have the same x-axis but different y-axis
            self.pressure_plot = self.temperature_plot.twinx()
            #Creates arrays for data storage for time elapsed, pressure, and temperature
            self.xtime = []
            self.pressure = []
            self.temperature = []
            ##Plots the two plots for temperature and pressure. Red plot for Temperature and Blue plot for Pressure.
            self.pressure_plot.plot(self.xtime, self.pressure, color = "blue", label = 'pressure')
            self.temperature_plot.plot(self.xtime, self.temperature, color = "red", label = 'temperature')
            ##Creates a legend for easy identification of both plots
            self.leg = self.graph_figure.legend(loc = 'upper left', facecolor = "#242526", 
                edgecolor = "#242526", bbox_to_anchor = (.115, 1.0))
            for text in self.leg.get_texts():
                text.set_color("#e4e6eb")
            self.graph_canvas.get_tk_widget().pack(fill="both",expand=True)
            ##Sets the background colors for the plots to be grey for dark mode aesthetic
            self.graph_figure.set_facecolor("#242526")
            self.temperature_plot.set_facecolor("#242526")
            self.temperature_plot.tick_params(axis = "y",colors = "Red")
            self.pressure_plot.tick_params(axis = "y", colors = "Blue")
            self.temperature_plot.tick_params(axis = "x", colors = "#e4e6eb")
            ##Sets the label and units for y-axis and x-axis of graph
            self.temperature_plot.set_ylabel("Temperature (°C)", color = "Red")
            self.pressure_plot.set_ylabel("Pressure (Psi)", color = "Blue")
            self.temperature_plot.set_xlabel("Time (s)", color = "#E4E6EB")
            self.temperature_plot.set_title("Lets Boil a Computer, Again!", color = "#ffffff",  fontsize = 30, fontweight = 20)
        

    def set_graph(self, newPressure, newTemperature, newTime):
        ##Allows for appending of new data to the graph but only displays the last 20 data points 
        # for easy of graph use and non-cluttering of display
        self.xtime = self.xtime[-20:]
        self.pressure = self.pressure[-20:]
        self.temperature = self.temperature[-20:]
        self.temperature.append(newTemperature)
        self.pressure.append(newPressure)
        self.xtime.append(newTime)       
        ##Plots the temperature and pressure with the correct x axis.
        self.pressure_plot.plot(self.xtime, self.pressure, color = "blue")
        self.temperature_plot.plot(self.xtime, self.temperature, color = "red")
        self.temperature_plot.set_xlim(self.xtime[0],self.xtime[-1], 1) 
        ##Sets the label and units for y-axis and x-axis of graph
        self.temperature_plot.set_ylabel("Temperature (°C)", color = 'Red')
        self.pressure_plot.set_ylabel("Pressure (Psi)", color = "blue")
        self.temperature_plot.set_xlabel("Time Samples at 10 Hz", color = "#E4E6EB")      
        ##Deletes and redraws the graph so that the graph looks animated and incoming data 
        #is reflected as soon as its collected.
        self.graph_canvas.draw()
        self.graph_canvas.flush_events()

    def draw_pump_gauge(self):
        press_label_frame = ttk.Frame(self.pump_pressure_frame)
        press_label_frame.pack()
        press_label = ttk.Label(press_label_frame, text="Pressure:")
        press_label.pack()
        self.press_value = ttk.Label(press_label_frame, text="NULL")
        self.press_value.pack()
        self.press_canvas = Canvas(
            self.pump_pressure_frame, width=200, height=200, borderwidth= 0, highlightthickness=0)
        # Create barometer
        self.press_canvas.create_oval(50, 50, 150, 150, width=10, outline="gray")
        self.press_canvas.create_arc(50, 50, 150, 150, start=135,
                                     extent=90, fill="green", width=0, outline="green")
        self.press_canvas.create_arc(50, 50, 150, 150, start=45,
                                     extent=90, fill="yellow", width=0, outline="yellow")
        self.press_canvas.create_arc(50, 50, 150, 150, start=315,
                                     extent=90, fill="red", width=0, outline="red")
        self.press_canvas.create_arc(50, 50, 150, 150, start=225,
                                     extent=90, fill="#d8d8d8", width=0, outline="#d8d8d8")
        self.press_canvas.pack()
        self.press_canvas.create_oval(80, 80, 120, 120, width=10,
                                      outline="#d8d8d8", fill="#d8d8d8")
        self.press_canvas.create_rectangle(
            90, 150, 110, 180, fill="gray", outline="gray")
        # Create needle
        needle_endpoint = self.needle_coords(225)
        self.needle = self.press_canvas.create_line(
            100, 100, needle_endpoint[0], needle_endpoint[1], fill="blue", width=3)
        self.press_canvas.create_oval(90, 90, 110, 110, fill="blue", width=0)
        # Dark background
        self.press_canvas.configure(bg="#18191A")

    def set_pump_pressure(self, new_press):
        """Sets the pressure and animates barometer accordingly"""
        # self.pressure = new_press
        self.press_value.config(text=new_press)
        new_press = abs(new_press)
        print(new_press)
        if new_press >= .05 and not self.control.koolance_on:
            self.control.koolance_on = True
            image = Image.open("koolance-on.png").resize((172, 49))
            self.koolance_image = ImageTk.PhotoImage(image)
            self.koolance_image_label.destroy()
            self.koolance_image_label = ttk.Label(
                self.title_bar, image=self.koolance_image)
            self.koolance_image_label.pack(side="left")
        elif new_press < .05 and self.control.koolance_on:
            self.control.koolance_on = False
            image = Image.open("koolance-off.png").resize((172, 49))
            self.koolance_image = ImageTk.PhotoImage(image)
            self.koolance_image_label.destroy()
            self.koolance_image_label = ttk.Label(
                self.title_bar, image=self.koolance_image)
            self.koolance_image_label.pack(side="left")
        if new_press > 3:
            new_press = 3
        theta = 225 - (new_press / 3) * 270
        needle_endpoint = self.needle_coords(theta)
        self.press_canvas.coords(
            self.needle, 100, 100, needle_endpoint[0], needle_endpoint[1])
    
    def draw_thermometer(self):
        self.temp_label_frame = Frame(self.temp_frame)
        self.temp_label_frame.pack()
        self.temp_label = ttk.Label(self.temp_label_frame, text="Temperature:")
        self.temp_label.pack()
        self.temp_value = ttk.Label(self.temp_frame, text="NULL")
        self.temp_value.pack()
        self.therm_canvas = Canvas(self.temp_frame, width=200, height=200, borderwidth= 0, highlightthickness=0)
        self.therm_canvas.create_rectangle(
            80, 20, 120, 160, fill="#e4e6eb", width=0)
        self.therm_circ = self.therm_canvas.create_oval(
            70, 140, 130, 200, fill="blue", width=0)
        # Create rectangle that will change size
        self.therm_rect = self.therm_canvas.create_rectangle(
            80, 140, 120, 160, fill="blue", width=0)
        self.therm_canvas.pack()
         # Dark background
        self.therm_canvas.configure(bg="#18191A")

    def set_temperature(self, new_temp):
        """Sets the temperature and adjusts thermometer animation accordingly"""
        # self.temperature = new_temp
        # Temperatures only visually supported between 20 and 
    # Adjust temperature value on GUI
        self.temp_value.config(text=new_temp)
        if new_temp < 20:
            new_temp = 20
        if new_temp > 60:
            new_temp = 60
       
        # Calculate height needed by rectangle to simulate where thermometer is
        height = (new_temp - 20) * 3
        # Update rectangle coordinates to change height
        self.therm_canvas.coords(self.therm_rect, 80, 140 - height, 120, 160)
        # Get a scaled color shift value based on temperature
        # Get red value in hex
        color_shift = int(((new_temp - 20) / 40.0) * 255)
        green = hex(color_shift)[2:]
        # If statement needed to give leading zero to single digit hex value
        if len(green) == 1:
            green = "0" + green
        # Red value won't change
        red = "00"
        # Get blue value in hex
        blue = hex(255 - color_shift)[2:]
        # If statement needed to give leading zero to single digit hex value
        if len(blue) == 1:
            blue = "0" + blue
        # Generate hex color
        new_color = f"#{red}{green}{blue}"
        # print(new_color)
        # print(f"Green = {color_shift}, Blue = {255 - color_shift}")
        # Update color
        self.therm_canvas.itemconfig(self.therm_rect, fill=new_color)
        self.therm_canvas.itemconfig(self.therm_circ, fill=new_color)

    def draw_flow_rate(self):
        #Creating the box for 
        self.flow_rate_label_frame = ttk.Frame(self.flow_rate_frame)
        self.flow_rate_label_frame.pack()
        self.flow_rate_label = ttk.Label(self.flow_rate_label_frame, text = "Flow Rate:")
        self.flow_rate_label.pack()
        self.flow_rate_value = ttk.Label(self.flow_rate_frame, text = "NULL")
        self.flow_rate_value.pack()
        self.flow_rate_canvas = Canvas(self.flow_rate_frame, width = 200, height = 200, highlightthickness= 0, borderwidth=0, background="grey")
        #self.flowrate_canvas.create_rectangle(80, 20, 120, 160, fill="#302c2d", width=0)
        self.flow_rate_canvas.pack()
        self.flow_rate_canvas.configure(bg="#302c2d")

        # Create barometer
        self.flow_rate_canvas.create_oval(50, 50, 150, 150, width=10, outline="grey")
        self.flow_rate_canvas.create_arc(50, 50, 150, 150, start=135,
                                     extent=90, fill="#d8d8d8", width=0, outline="#d8d8d8")
        self.flow_rate_canvas.create_arc(50, 50, 150, 150, start=45,
                                     extent=90, fill="#d8d8d8", width=0, outline="#d8d8d8")
        self.flow_rate_canvas.create_arc(50, 50, 150, 150, start=315,
                                     extent=90, fill="#d8d8d8", width=0, outline="#d8d8d8")
        self.flow_rate_canvas.create_arc(50, 50, 150, 150, start=225,
                                    extent=90, fill="#d8d8d8", width=0, outline="#d8d8d8")
        self.flow_rate_canvas.pack()
        self.flow_rate_canvas.create_oval(80, 80, 120, 120, width=10,
                                      outline="#d8d8d8", fill="#d8d8d8")
        self.flow_rate_canvas.create_rectangle(
            90, 150, 110, 180, fill="gray", outline="gray")
        # Create needle
        self.needle_endpoint = self.needle_coords(225)
        self.needle = self.flow_rate_canvas.create_line(
            100, 100, self.needle_endpoint[0], self.needle_endpoint[1], fill="blue", width=3)
        self.flow_rate_canvas.create_oval(90, 90, 110, 110, fill="blue", width=0)

        # Creating the tick marks on the flowrate gauge
        self.flow_rate_canvas.create_line(100, 60, 100, 50, fill = "Black", width=3)
        self.flow_rate_canvas.create_line(60, 100, 50, 100, fill = "Black", width=3)
        self.flow_rate_canvas.create_line(140, 100, 150, 100, fill = "Black", width=3)
        self.flow_rate_canvas.create_line(73, 73, 65, 65, fill = "Black", width=3)
        self.flow_rate_canvas.create_line(127, 127, 135, 135, fill = "Black", width=3)
        self.flow_rate_canvas.create_line(73, 127, 65, 135, fill = "Black", width=3)
        self.flow_rate_canvas.create_line(127, 73, 135, 65, fill = "Black", width=3)
        # Creating the numbers by the tick marks on the flowrate gauge change as necessary
        self.flow_rate_canvas.create_text(78, 122, text="0") #done
        self.flow_rate_canvas.create_text(65, 100, text="1") #done
        self.flow_rate_canvas.create_text(78, 78, text="2") #done
        self.flow_rate_canvas.create_text(100, 70, text="3") #done
        self.flow_rate_canvas.create_text(122, 78, text="4") #done
        self.flow_rate_canvas.create_text(135, 100, text="5") #done
        self.flow_rate_canvas.create_text(122, 122, text="6") #done
        # Dark background
        self.flow_rate_canvas.configure(bg="#18191A")
        
    def set_flow_rate(self, new_rate): 
        #self.flow_rate = new_rate
        self.flow_rate_value.config(text = new_rate)
        new_rate = abs(new_rate)
        self.theta = 225 - (new_rate / 6) * 270
        self.needle_endpoint = self.needle_coords(self.theta)
        self.flow_rate_canvas.coords(self.needle,100,100, self.needle_endpoint[0], self.needle_endpoint[1])

    def set_fluid_level(self, new_level):
        self.fluid_level_value.config(text = new_level)

    def needle_coords(self, theta):
        """Given an angle (degrees), calculates coordinates of endpoint of line of needle"""
        # Needle length
        needle_length = 40
        alpha = math.radians(theta - 180)
        delta_x = needle_length * math.cos(alpha)
        delta_y = needle_length * math.sin(alpha)
        return (100 - delta_x, 100 + delta_y)
    def on_closing(self):
        print("Close")
        self.master.destroy()

def main():
    root = Tk()
    control = None
    gui = GUI(root, control)
    root.state('zoomed')
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()