import threading
import time
import serial
import serial.tools.list_ports
from datetime import datetime
from tkinter import Tk
from gui import GUI
import pandas as pd


class Control():
    def __init__(self, arduino):
        self.arduino = arduino
        self.time_start = 0
        self.time_duration = 0
        self.pump_on = False
        self.koolance_on = False
        self.override = False
        self.running = True
        self.data = []

    def set_gui(self, gui):
        self.gui = gui

    def manage_input(self):
        file_out = open("data.csv", "w")
        file_out.write("Timestamp, Temperature, Pressure In, Pressure Out, Pressure Differential, Flow Rate, Fluid Level\n")
        while self.running:
            # Receive data from the Arduino
            receive_string = self.arduino.readline().decode('utf-8').rstrip()
            time.sleep(.1)
            if not self.override:
                self.check_pump()
            # Print the data received from Arduino to the terminal
            self.arduino.reset_input_buffer()
            line_split = receive_string.split()
            if len(line_split) == 10:
                temperature = float(line_split[1])
                pressure_in = float(line_split[3])
                pressure_out = float(line_split[5])
                pressure_diff = round(pressure_in - pressure_out, 2)
                flow_rate = float(line_split[7])
                # fluid_level = float(line_split[9])
                fluid_level = float(22)
                timestamp = datetime.now()
                self.gui.set_temperature(temperature)
                self.gui.set_pump_pressure(pressure_diff)
                self.gui.set_flow_rate(flow_rate)
                self.gui.set_fluid_level(fluid_level)
                self.gui.set_graph(pressure_diff, temperature, timestamp)
                self.data.append([timestamp] + line_split)
                line = f"{timestamp}, {temperature}, {pressure_in}, {pressure_out}, {pressure_diff}, {flow_rate}, {fluid_level}\n"
                file_out.write(line)
                file_out.flush()


    def toggle_override(self):
        self.override = not self.override

    def toggle_pump(self):
        print("Toggle Pump")
        code = "FILTER"
        self.arduino.write(code.encode('utf-8'))
        self.pump_on = not self.pump_on

    def apply_settings(self, time_start, time_duration):
        print("Preparing to apply settings to Arduino")
        self.time_start = time_start
        self.time_duration = time_duration

    def on_closing(self):
        print("Close")
        self.running = False
        self.master.destroy()

    def check_pump(self):
        minute = datetime.now().minute
        if self.time_duration > 0:
            if not self.pump_on:
                if minute >= self.time_start and minute < self.time_start + self.time_duration:
                    self.toggle_pump()
            elif minute < self.time_start or minute >= self.time_start + self.time_duration:
                self.toggle_pump()


def main():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print(ports)
    arduino = serial.Serial(port=ports[0], baudrate=115200, timeout=.1)
    time.sleep(1)
    root = Tk()
    control = Control(arduino)
    gui = GUI(root, control)
    control.set_gui(gui)
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    thread1 = threading.Thread(target=control.manage_input)
    thread1.start()
    
    root.mainloop()
    thread1.join()


if __name__ == "__main__":
    main()
