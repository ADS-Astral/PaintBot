
class MotorControl:

    serial = None

    def __init__(self, serial):
        self.serial = serial
        self.serial.close()
        self.serial.open()
        pass

    def __del__(self):
        self.serial.close()
        pass

    def write(self, signal):
        byte = str(signal).encode('utf-8')
        self.serial.write(byte)
        self.serial.flush()
        read = self.serial.readline()
        # if read != b'':
        #     break
        print(read)
        pass

    STATE_STOP = 0

    def Stop(self):
        self.write(self.STATE_STOP)
        pass

    STATE_FORWARD = 1

    def MoveForward(self):
        self.write(self.STATE_FORWARD)
        pass

    STATE_REVERSE = 2

    def MoveReverse(self):
        self.write(self.STATE_REVERSE)
        pass

    STATE_LEFT = 3

    def MoveLeft(self):
        self.write(self.STATE_LEFT)
        pass

    STATE_RIGHT = 4

    def MoveRight(self):
        self.write(self.STATE_RIGHT)
        pass
