from smbus2 import SMBus


class MotorControl:

    address = None
    bus = None

    def __init__(self):
        self.address = 0x8
        self.bus = SMBus(1)
        pass

    MOVE_FORWARD = 0

    def MoveForward(self):
        self.bus.write_byte(self.address, self.MOVE_FORWARD)
        pass

    MOVE_REVERSE = 1

    def MoveReverse(self):
        self.bus.write_byte(self.address, self.MOVE_REVERSE)
        pass

    MOVE_LEFT = 2

    def MoveLeft(self):
        self.bus.write_byte(self.address, self.MOVE_LEFT)
        pass

    MOVE_RIGHT = 3

    def MoveRight(self):
        self.bus.write_byte(self.address, self.MOVE_RIGHT)
        pass
