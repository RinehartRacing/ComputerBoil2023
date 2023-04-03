##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 
from datetime import datetime
import serial  # sudo pip install pyserial should work
import serial.tools.list_ports
ports = [comport.device for comport in serial.tools.list_ports.comports()]
print(ports)
ser = serial.Serial(port=ports[0], baudrate=9600)
write_to_file_path = "output.txt"

output_file = open(write_to_file_path, "w+")
while True:
    line = ser.readline()
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    print(line)
    # output_file.write(f"{datetime.now()} {line}")