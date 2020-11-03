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
        self.data = []
        self.wall_data = [0] * self.modules
        self.floor_data = [0] * self.modules
        self.room = 0
        self.wall = 0
        self.floor = 0
        self.out = [0] * self.modules
        self.timeout = self.get_timeout()
        self.image_num = 0

    def wall_num(self):
        sum = 0
        for i in range(1, len(self.data)):
            # byte_data = self.data[i] * (2 ** (8 * i))
            if self.data[i] > 15:
                sum += (math.log2(self.data[i]) - 3) + i * 4
                self.wall_data[i] = self.data[i]
        return sum

    def floor_num(self):
        sum = 0
        for i in range(1, len(self.data)):
            # byte_data = self.data[i] * (2 ** (8 * i))
            if 0 < self.data[i] < 16:
                sum += (math.log2(self.data[i])) + i * 4
                self.floor_data[i] = self.data[i]
        return sum

    def get_timeout(self):
        return self.config['timeout'] * 25

    def process(self):
        self.timeout -= 1
        self.data = self.spi.readbytes(self.modules)
        print('ROOM - ', self.room)
        print('WALL - ', self.wall)
        print('FLOOR - ', self.floor)
        self.spi.writebytes(self.out[::-1])
        self.IO.output(self.cs, 1)
        time.sleep(0.01)
        self.IO.output(self.cs, 0)
        time.sleep(0.01)
        self.IO.output(self.cs, 1)

        if (self.floor_num() > 0) and self.room > 0:
            self.floor = self.floor_num()
            self.timeout = self.get_timeout()
            for i in range(self.modules):
                self.out[i] = self.wall_data[i] + self.floor_data[i]
            self.out[0] = self.room

        if (self.wall_num() > 0) and self.room > 0:
            self.wall = self.wall_num()
            self.timeout = self.get_timeout()
            for i in range(self.modules):
                self.out[i] = self.wall_data[i] + self.floor_data[i]
            self.out[0] = self.room

        if self.data[0] > 0:
            self.room = self.data[0]
        if self.timeout == 0:
            self.room = 0
            self.floor_data = [0] * self.modules
            self.wall_data = [0] * self.modules
            self.out = [0] * self.modules

        return int(self.image_num)
