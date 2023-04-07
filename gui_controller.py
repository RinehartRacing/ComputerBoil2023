import threading
import serial
import serial.tools.list_ports
from tkinter import Tk
from gui import GUI
def read(arduino):
    try:
        data = arduino.readline().decode("ascii")
        return data
    except UnicodeDecodeError:
        return ""
def control_gui(gui, sensor_code, value):
    if sensor_code == "T":
        gui.set_temperature(value)
        # gui.set_graph(value, 3, )
    elif sensor_code == "PD":
        gui.set_pump_pressure(value)
    elif sensor_code == "FR":
        gui.set_flow_rate(value)
    elif sensor_code == "FL":
        gui.set_fluid_level(value)
def manage_input(gui, arduino):
    while True:
        line = read(arduino)
        line_split = line.split()
        if len(line_split) == 2:
            sensor_code = line_split[0]
            value = float(line_split[1])
            control_gui(gui, sensor_code, value)


def main():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print(ports)
    arduino = serial.Serial(port=ports[0], baudrate=9600, timeout=.01)

    root = Tk()
    gui = GUI(root)

    thread1 = threading.Thread(target=manage_input, 
                           args=(gui, arduino))
    thread1.start()
    root.mainloop()
    thread1.join()
if __name__ == "__main__":
    main()