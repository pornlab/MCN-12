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
        self.read_cmd = []
        self.room = 0
        self.out = []
        self.timeout = self.get_timeout()
        self.image_num = 0

    def sum(self):
        a = 0
        for i in range(len(self.read_cmd)):
            a += self.read_cmd[i] * (2 ** (8 * i))
        return a

    def get_timeout(self):
        return self.config['timeout'] * 25

    def process(self):
        self.timeout -= 1
        self.data = self.spi.readbytes(self.modules)
        for i in range(1, len(self.modules)):
            self.read_cmd.append(self.data[i])
        print('DATA- ', self.data)
        print('ROOM - ', self.room)
        print('CMD = ', self.read_cmd)
        print('OUT - ', self.out)
        self.IO.output(self.cs, 1)
        time.sleep(0.01)
        self.IO.output(self.cs, 0)
        time.sleep(0.01)
        self.IO.output(self.cs, 1)
        if self.data[0] > 0:
            self.room = self.data[0]
            self.out = self.read_cmd
            self.out.insert(0, self.room)
        if self.sum() > 0:
            print("in ", self.read_cmd)
            self.timeout = self.get_timeout()
            self.out = self.read_cmd
            self.out.insert(0, self.room)
            for i in range(self.modules):
                if self.read_cmd[i] != 0:
                    self.image_num = 1 + (i * 8) + math.log2(sum(self.read_cmd))
        if self.timeout == 0:
            self.image_num = 0
            self.room = 0
            self.out = [0] * self.modules

        self.spi.writebytes(self.out[::-1])
        return int(self.image_num)
