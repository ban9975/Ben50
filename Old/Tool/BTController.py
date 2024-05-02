import serial
import serial.tools.list_ports
def list_all_ports():
    ports = serial.tools.list_ports.comports()
    portList = []
    for port in ports:
        portList.append(port.device)
    return portList

class BTController:
    def __init__(self) -> None:
        pass
    def do_connect(self, port):
        while not self.connect(port):
            print('connecting')
            self.connect(port)
    def connect(self, port):
        try:
            self.ser = serial.Serial(port,38400,timeout=2)
            print("connect success")
            print(port)
            self.write('0')
            return True
        except serial.serialutil.SerialException as ex:
            print("fail to connect")
            print(ex)
            print("")
            return False
    def __del__(self):
        if self.ser.is_open:
            self.ser.close()

    def write(self,output):
        if output.isdigit():
            send = int(output).to_bytes(1, 'little')
        else:
            send = output.encode("utf-8")
        self.ser.write(send)

    def read(self):
        waiting = self.ser.in_waiting
        if waiting >= 0:
            rv = self.ser.read(2)
            rv=int.from_bytes(rv, byteorder='big', signed=False)
            return rv
        

bt = BTController()