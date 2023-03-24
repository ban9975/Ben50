import BT

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        while(not self.ser.do_connect("COM12")):
            self.ser.do_connect("COM12")
        self.write('0')

    def read(self):
        return self.ser.SerialReadInt()

    def end_process(self):
        self.ser.disconnect()

    def write(self, input):
        return self.ser.SerialWrite(input)