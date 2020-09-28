import spidev

class xx74xx165_driver:
    def __init__(self, bus=0, device=1):
        self.bus = bus
        self.device = device
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0
        pass

    def read_chip(self, pin):
        pass

    def reset_chip(self):
        pass

