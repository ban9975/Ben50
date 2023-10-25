import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)
ser = serial.Serial('/dev/cu.hc05', 9600, timeout=2)
while True:
    data = ser.read(1)
    if data:
        print(data)