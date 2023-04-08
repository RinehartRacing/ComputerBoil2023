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
def control_gui(gui, sensor_code, value, data_dict):
    data_dict[sensor_code] = value
    print(data_dict)
    if sensor_code == "T": 
        gui.set_temperature(value)
        # gui.set_graph(value, 3, )
    elif sensor_code == "PI":
        gui.set_pump_pressure(round(value - data_dict["PO"], 2))
    elif sensor_code == "PO":
        gui.set_pump_pressure(round(data_dict["PI"] - value, 2))
    elif sensor_code == "FR":
        gui.set_flow_rate(value)
    elif sensor_code == "FL":
        gui.set_fluid_level(value)
    else:
        print(f"Rogue sensor code {sensor_code} with value {value}")
def manage_input(gui, arduino):
    data_dict = {"T": None, "PI": 13, "PO": 13, "FR": None, "FL": None}
    global temperature
    global pressure_in
    global pressure_out
    global flow_rate
    global fluid_level
    buffer = []
    while True:
        line = read(arduino)
        line_split = line.split()
        if len(line_split) == -1 and line[-1] == " ":
            for field in line_split:
                buffer.append(field)
                if len(buffer) == 2:
                    print(buffer)
                    control_gui(gui, buffer[0], float(buffer[1]), data_dict)
                    buffer = []
        else:
            line_split += read(arduino).split()
            print(line_split)

        # line_split = line.split()
        # if len(line_split) == 2:
        #     sensor_code = line_split[0]
        #     value = float(line_split[1])
        #     control_gui(gui, sensor_code, value)


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