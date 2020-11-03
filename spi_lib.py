import spidev
import math
import RPi.GPIO as IO
import time
import os
from PIL import Image

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
        self.room_data = 0
        self.wall = 0
        self.floor = 0
        self.room = 0
        self.out = [0] * self.modules
        self.timeout = self.get_timeout()
        self.image_path = os.path.join('images', 'room_0', 'wall_0', '0.png')

    def wall_num(self):
        sum = 0
        for i in range(1, len(self.data)):
            if self.data[i] > 15:
                self.wall_data = [0] * self.modules
                sum += (math.log2(self.data[i]) - 3) + (i - 1) * 4
                self.wall_data[i] = self.data[i]

        return int(sum)

    def floor_num(self):
        sum = 0
        for i in range(1, len(self.data)):
            if 0 < self.data[i] < 16:
                self.floor_data = [0] * self.modules
                sum += 1 + (math.log2(self.data[i])) + (i - 1) * 4
                self.floor_data[i] = self.data[i]

        return int(sum)

    def get_timeout(self):
        return self.config['timeout'] * 25

    def process(self):
        self.timeout -= 1
        self.data = self.spi.readbytes(self.modules)
        # print('ROOM - ', self.room)
        # print('WALL - ', self.wall)
        # print('FLOOR - ', self.floor)
        self.spi.writebytes(self.out[::-1])
        self.IO.output(self.cs, 1)
        time.sleep(0.01)
        self.IO.output(self.cs, 0)
        time.sleep(0.01)
        self.IO.output(self.cs, 1)
        floor = self.floor_num()
        wall = self.wall_num()
        if (floor > 0) and self.room_data > 0:
            #self.floor_data = [0] * self.modules
            self.floor = floor
            self.timeout = self.get_timeout()
            # self.out = [0] * self.modules
            for i in range(self.modules):
                self.out[i] = self.floor_data[i] + self.wall_data[i]
            self.out[0] = self.room_data

        if (wall > 0) and self.room_data > 0:
            #self.wall_data = [0] * self.modules
            self.wall = wall
            self.timeout = self.get_timeout()
            # self.out = [0] * self.modules
            for i in range(self.modules):
                self.out[i] = self.wall_data[i] + self.floor_data[i]
            self.out[0] = self.room_data

        if self.data[0] > 0:
            self.room_data = self.data[0]
            self.out[0] = self.room_data
            self.room = int(1 + math.log2(self.room_data))

        if self.timeout == 0:
            self.room_data = 0
            self.floor_data = [0] * self.modules
            self.wall_data = [0] * self.modules
            self.wall = 0
            self.floor = 0
            self.room = 0
            self.out = [0] * self.modules

        self.image_path = os.path.join('images', 'room {}'.format(self.room), 'wall {}'.format(self.wall),
                                       '{}.png'.format(self.floor))
        return self.image_path
