import threading
import serial
import time
import serial.tools.list_ports;
from tkinter import Tk
from gui import GUI
from gui_test import test_temperature
import numpy as np


def read(arduino):
    #arduino.write(bytes(x, 'utf-8'))
    #time.sleep(0.05)
    data = arduino.readline().decode("ascii")
    return data

def test_temperature(gui, arduino):
    print("Hello")
    while True:
        value = read(arduino)
        if value != "" and value.replace('.', '', 1).isdigit():
            value = float(value)
            print(f"Temperature = {value}")
            gui.set_temperature(value)

def test_graph(gui, arduino):
    print("Hello")
    i = 0
    while True:
        value = read(arduino)
        #print(value)
        if value != "" and value.replace('.', '', 1).isdigit():
            value = float(value)
            print(f"Temperature = {value}")
            gui.set_graph(value, np.cos(i), i)
            i += 1

def main():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print(ports)
    arduino = serial.Serial(port=ports[0], baudrate=9600, timeout=.01)

    root = Tk()
    gui = GUI(root)
    thread1 = threading.Thread(target=test_temperature, 
                           args=(gui, arduino))
    thread2 = threading.Thread(target=test_graph, 
                            args=(gui,arduino))
    #thread1.start()
    thread2.start()

    root.mainloop()
    #thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
