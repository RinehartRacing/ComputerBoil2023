import threading
import time
import serial
import serial.tools.list_ports
from datetime import datetime
from tkinter import Tk
from gui import GUI

"""
    Team 23016 - Let's Boil a Computer Again!
    Rusty Rinehart, Jesus Arias, Chris Bremser, Prasanna Raut, Sean Brown
    This file is responsible for connecting the Arduino to the Raspberry Pi
"""
class Control():
    def __init__(self, arduino):
        # Object for executing Arduino Serial commands
        self.arduino = arduino
        # Duty cycle status variables
        self.time_start = 0
        self.time_duration = 0
        # Booleans to keep track of high-power relay status
        self.pump_on = False
        self.koolance_on = False
        self.override = False
        self.running = True

    def set_gui(self, gui):
        """Used to give gui object reference to controller"""
        self.gui = gui

    def manage_input(self):
        """This method takes in Arduino data packets and tells the GUI or Arduino what to do with them"""
        # Create a CSV file to log data
        file_out = open("data.csv", "w")
        # Create header row of CSV file
        file_out.write("Timestamp, Temperature, Pressure In, Pressure Out, Pressure Differential, Flow Rate, Fluid Level\n")
        # Main loop of controller
        while self.running:
            # Receive data from the Arduino
            receive_string = self.arduino.readline().decode('utf-8').rstrip()
            time.sleep(.1)
            # Runs if pump is 
            if not self.override:
                self.check_pump()
            # Discard extra packets in Serial line
            self.arduino.reset_input_buffer()
            line_split = receive_string.split()
            # Check if packet is complete
            if len(line_split) == 10:
                temperature = float(line_split[1])
                pressure_in = float(line_split[3])
                pressure_out = float(line_split[5])
                pressure_diff = round(pressure_in - pressure_out, 2)
                flow_rate = float(line_split[7])
                fluid_level = float(line_split[9])
                # Grab current timestamp
                timestamp = datetime.now()
                # Update GUI
                self.gui.set_temperature(temperature)
                self.gui.set_pump_pressure(pressure_diff)
                self.gui.set_flow_rate(flow_rate)
                self.gui.set_fluid_level(fluid_level)
                self.gui.set_graph(pressure_diff, temperature, timestamp)
                # Add packet of data to CSV
                line = f"{timestamp}, {temperature}, {pressure_in}, {pressure_out}, {pressure_diff}, {flow_rate}, {fluid_level}\n"
                file_out.write(line)
                file_out.flush()


    def toggle_override(self):
        """This method is called when filter button is pressed"""
        self.override = not self.override

    def toggle_pump(self):
        """This method is called when pump needs to be toggled"""
        # Send the packet "FILTER" to Arduino to tell it to turn pump on
        code = "FILTER"
        self.arduino.write(code.encode('utf-8'))
        self.pump_on = not self.pump_on

    def apply_settings(self, time_start, time_duration):
        """This method updates duty cycle settings"""
        self.time_start = time_start
        self.time_duration = time_duration

    def on_closing(self):
        """This method is called when GUI is closed"""
        print("Close")
        self.running = False
        self.master.destroy()

    def check_pump(self):
        """This method checks if the pump is supposed to be on based on settings"""
        minute = datetime.now().minute
        if self.time_duration > 0:
            if not self.pump_on:
                if minute >= self.time_start and minute < self.time_start + self.time_duration:
                    self.toggle_pump()
            elif minute < self.time_start or minute >= self.time_start + self.time_duration:
                self.toggle_pump()


def main():
    # Check for devices plugged in
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print(ports)
    # Grab Arduino serial port object
    arduino = serial.Serial(port=ports[0], baudrate=115200, timeout=.1)
    time.sleep(1)
    # Create root Tkinter frame
    root = Tk()
    # Create Controller object
    control = Control(arduino)
    # Create GUI object
    gui = GUI(root, control)
    # Pass GUI object to Control object
    control.set_gui(gui)
    # Create action listner for when window is closed
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    # Run main loop on its own thread
    thread1 = threading.Thread(target=control.manage_input)
    thread1.start()
    
    root.mainloop()
    thread1.join()


if __name__ == "__main__":
    main()
