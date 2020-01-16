
class MotorControl:

    STATE_STOP = 0
    STATE_FORWARD = 1
    STATE_REVERSE = 2
    STATE_LEFT = 3
    STATE_RIGHT = 4

    serial = None

    def __init__(self, serial):
        self.serial = serial
        pass

    def __del__(self):
        self.serial.close()
        pass

    def write(self, signal):
        byte = str(signal).encode('utf-8')
        self.serial.write(byte)
        pass

    def Stop(self):
        self.write(self.STATE_STOP)
        pass

    def MoveForward(self):
        self.write(self.STATE_FORWARD)
        pass

    def MoveReverse(self):
        self.write(self.STATE_REVERSE)
        pass

    def MoveLeft(self):
        self.write(self.STATE_LEFT)
        pass

    def MoveRight(self):
        self.write(self.STATE_RIGHT)
        pass
