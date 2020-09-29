from spi_lib import SPI
import threading
import pygame


class Routine:
    def __init__(self):
        self.spi = SPI()
        self.image = 0
        self.process = threading.Thread(target=self.routine, args=(None, ))
        self.process.start()

    def routine(self, a):
        while 1:
            self.image = self.spi.process()
            if self.image != 0:
                print(self.image)
                pass
