from spi_lib import SPI
import threading
from graphics import Graphics
import os


class Routine:
    def __init__(self):
        self.spi = SPI()
        self.image = os.path.join('images', 'room_0', 'wall_0', '0.jpg')
        self.graph = Graphics()
        self.done = False
        self.process1 = threading.Thread(target=self.routine_spi, args=(None, ))
        self.process2 = threading.Thread(target=self.routine_graph, args=(None,))
        self.process1.start()
        self.process2.start()

    def routine_spi(self, a):
        while not self.done:
            self.image = self.spi.process()

    def routine_graph(self, a):
        while not self.done:
            self.done = self.graph.load_image(self.image)
            if self.image != 0:
                pass
