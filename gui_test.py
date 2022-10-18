"""
    Engineering 498
    Let's Boil a Computer
    Rusty Rinehart
    Chris Bremser
    Jesus Arias
    Prasanna Raut
    Sean Brown

    This file tests the functionality of the GUI via software
"""
from tkinter import Tk
from gui import GUI



def test_temperature(gui):
    while True:
        for i in range(20, 60):
            print(f"Temperature = {i}")
            gui.set_temperature(i)
            # Input waits for user to hit enter in terminal so we can visualize each changing temperature
            input()
        for i in range(60, 20, -1):
            print(f"Temperature = {i}")
            gui.set_temperature(i)
            input()

def test_pressure(gui):
    while True:
        for i in range(-30, 30, 1):
            print(i / 10.0)
            gui.set_pump_pressure(i / 10.0)
            
            input()

def test_solenoid(gui):
    while True:
        gui.set_solenoid(True)
        print("Solenoid On")
        input()
        gui.set_solenoid(False)
        print("Solenoid Off")
        input()

# def test_graph(gui):
#     while True:
#         for i in range (0, 100, 1):
#         gui.graph_display()
#         print(i)
#         input()



def main():
    root = Tk()
    gui = GUI(root)
    #test_temperature(gui)
    test_pressure(gui)
    #test_solenoid(gui)
    root.mainloop()


if __name__ == "__main__":
    main()
