import threading
import serial
import time
import serial.tools.list_ports;
from tkinter import Tk
from gui import GUI
from gui_test import test_temperature

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

def main():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    arduino = serial.Serial(port="COM3", baudrate=9600, timeout=.1)

    root = Tk()
    gui = GUI(root)
    thread1 = threading.Thread(target=test_temperature, 
                           args=(gui, arduino))
    thread1.start()

    root.mainloop()
    thread1.join()

if __name__ == "__main__":
    main()
