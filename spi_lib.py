import spidev
import math


class SPI:
    def __init__(self):
        self.config = eval(' '.join(open('config.txt', 'r').read().split('\n')))
        self.bus = self.config['spi']['bus']
        self.device = self.config['spi']['device']
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = self.config['spi']['max_speed_hz']
        self.spi.mode = self.config['spi']['spi_mode']
        self.modules = self.config['modules']

        self.read_cmd = [0] * self.modules
        pass

    def sum(self):
        a = 0
        for i in range(len(self.read_cmd)):
            a += self.read_cmd[i]
        return a

    def process(self):
        image_num = 0
        self.read_cmd = self.spi.readbytes(self.modules)
        if self.sum() > 0:
            self.spi.writebytes(self.read_cmd)
            for i in range(self.modules):
                if self.read_cmd[i] != 0:
                    image_num = i + math.log2(self.read_cmd[i])
        return image_num
