import threading
import time
import serial
import serial.tools.list_ports
from tkinter import Tk
from gui import GUI


def read(arduino):
    try:
        data = arduino.readline().decode("utf-8")
        return data
    except UnicodeDecodeError:
        return ""


def manage_input(gui, arduino):
    while True:
        send_string = "REQ"

        # Send the string. Make sure you encode it before you send it to the Arduino.
        arduino.write(send_string.encode('utf-8'))
        
        # Do nothing for 500 milliseconds (0.5 seconds)
        # time.sleep(0.01)
        time.sleep(.2)
        # Receive data from the Arduino
        receive_string = arduino.readline().decode('utf-8').rstrip()
            
        # Print the data received from Arduino to the terminal
        print(receive_string)


def main():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    print(ports)
    arduino = serial.Serial(port=ports[0], baudrate=2000000, timeout=.1)
    time.sleep(.1)
    root = Tk()
    gui = GUI(root)

    thread1 = threading.Thread(target=manage_input, 
                           args=(gui, arduino))
    thread1.start()
    # root.mainloop()
    thread1.join()
if __name__ == "__main__":
    main()