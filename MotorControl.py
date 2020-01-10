import serial


class MotorControl:

    serial = None

    def __init__(self, serial_port):
        self.serial = serial.Serial(
            port=serial_port,
            baudrate=57600,
            timeout=1)
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

    STOP = 0

    def Stop(self):
        self.write(self.STOP)
        pass

    MOVE_FORWARD = 1

    def MoveForward(self):
        self.write(self.MOVE_FORWARD)
        pass

    MOVE_REVERSE = 2

    def MoveReverse(self):
        self.write(self.MOVE_REVERSE)
        pass

    MOVE_LEFT = 3

    def MoveLeft(self):
        self.write(self.MOVE_LEFT)
        pass

    MOVE_RIGHT = 4

    def MoveRight(self):
        self.write(self.MOVE_RIGHT)
        pass
