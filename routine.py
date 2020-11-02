from spi_lib import SPI
import threading
from graphics import Graphics


class Routine:
    def __init__(self):
        self.spi = SPI()
        self.image = 0
        self.graph = Graphics()
        self.process = threading.Thread(target=self.routine_spi, args=(None, ))
        self.process = threading.Thread(target=self.routine_graph, args=(None,))
        self.process.start()

    def routine_spi(self, a):
        while 1:
            self.image = self.spi.process()

    def routine_graph(self, a):
        while 1:
            self.graph.load_image(self.image)
            if self.image != 0:
                print(self.image)
                pass
