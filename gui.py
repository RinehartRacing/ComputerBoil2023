
"""
    Engineering 498
    Let's Boil a Computer
    Rusty Rinehart
    Chris Bremser
    Jesus Arias
    Prasanna Raut
    Sean Brown
"""
from tkinter import Canvas, Label, PhotoImage, Tk, ttk


class GUI:
    """
        This class holds all GUI information
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Let's Boil a Computer Again")
        self.temp_display()
        self.graph_display()
        self.press_display()
        self.sol_display()
        self.fluid_display()
        self.settings_display()

    def temp_display(self):
        temp_label = ttk.Label(self.master, text="Temperature:")
        temp_label.grid(row=0, column=0)
        temp_value = ttk.Label(self.master, text="NULL")
        temp_value.grid(row=1, column=0)
        self.temp_image = PhotoImage(file="thermometer.png").subsample(4, 4)
        image_label = ttk.Label(self.master, image=self.temp_image)
        image_label.grid(row=2, column=0)

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
