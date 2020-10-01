import spidev
import math
import RPi.GPIO as IO
import time

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
        self.cs = self.config['spi']['cs_pin']
        self.IO = IO
        self.IO.setmode(IO.BCM)
        self.IO.setwarnings(False)
        self.IO.setup(self.cs, 0)
        self.IO.output(self.cs, 0)
        self.read_cmd = [0] * self.modules

    def sum(self):
        a = 0
        for i in range(len(self.read_cmd)):
            a += self.read_cmd[i] * (2 ** (8 * i))
        return a

    def process(self):
        image_num = 0
        self.IO.output(self.cs, 1)
        time.sleep(0.1)
        self.read_cmd = self.spi.readbytes(self.modules)
        print(self.read_cmd)
        time.sleep(0.1)
        self.IO.output(self.cs, 0)
        time.sleep(0.1)
        if self.sum() > 0:
            self.IO.output(self.cs, 1)
            time.sleep(0.1)
            self.spi.writebytes(self.read_cmd)
            time.sleep(0.1)
            self.IO.output(self.cs, 0)
            time.sleep(0.1)
            for i in range(self.modules):
                if self.read_cmd[i] != 0:
                    image_num = i + math.log2(sum(self.read_cmd[i]))
        return image_num
