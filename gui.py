
"""
    Engineering 498
    Let's Boil a Computer
    Rusty Rinehart
    Chris Bremser
    Jesus Arias
    Prasanna Raut
    Sean Brown
"""
from tkinter import Canvas, PhotoImage, Tk, ttk


class GUI:
    """
        This class holds all GUI information
    """

    def __init__(self, master):
        self.master = master

        # Attributes
        self.temperature = None

        self.master.title("Let's Boil a Computer Again")
        self.temp_display()
        self.graph_display()
        self.press_display()
        self.sol_display()
        self.fluid_display()
        self.settings_display()
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=10)
        self.master.grid_rowconfigure(0, weight=10)

    def temp_display(self):
        temp_label = ttk.Label(self.master, text="Temperature:")
        temp_label.grid(row=0, column=0)
        self.temp_value = ttk.Label(self.master, text="NULL")
        self.temp_value.grid(row=1, column=0)
        self.therm_canvas = Canvas(self.master, width=100, height=100)
        self.therm_canvas.create_rectangle(
            40, 10, 60, 80, fill="white", width=0)
        self.therm_circ = self.therm_canvas.create_oval(
            35, 70, 65, 100, fill="black", width=0)
        # Create rectangle that will change size
        self.therm_rect = self.therm_canvas.create_rectangle(
            40, 70, 60, 80, fill="black", width=0)
        self.therm_canvas.grid(row=2, column=0)

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

    def graph_display(self):
        graph_label = ttk.Label(self.master, text="Graph Here")
        graph_label.grid(row=0, column=1, rowspan=3, columnspan=2)

    def press_display(self):
        press_label = ttk.Label(self.master, text="Pressure:")
        press_label.grid(row=0, column=3)
        press_value = ttk.Label(self.master, text="NULL")
        press_value.grid(row=1, column=3)
        canvas = Canvas(self.master, width=100, height=100)
        canvas.create_oval(25, 25, 75, 75)
        canvas.grid(row=2, column=3)

    def sol_display(self):
        sol_label = ttk.Label(self.master, text="Solenoid:")
        sol_label.grid(row=3, column=0)
        sol_value = ttk.Label(self.master, text="NULL")
        sol_value.grid(row=3, column=1)
        canvas = Canvas(self.master, width=100, height=100)
        canvas.create_oval(25, 25, 75, 75)
        canvas.grid(row=4, column=0)

    def fluid_display(self):
        fluid_label = ttk.Label(self.master, text="Fluid Level:")
        fluid_label.grid(row=3, column=2)
        fluid_value = ttk.Label(self.master, text="NULL")
        fluid_value.grid(row=3, column=3)
        canvas = Canvas(self.master, width=100, height=100)
        canvas.create_rectangle(25, 10, 75, 90)
        canvas.grid(row=4, column=3)

    def settings_display(self):
        settings_button = ttk.Button(self.master, text="Settings")
        settings_button.grid(row=4, column=1)
        time_label = ttk.Label(self.master, text="Current Time")
        time_label.grid(row=4, column=2)


def main():
    root = Tk()
    gui = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
