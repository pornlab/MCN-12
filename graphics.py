import pygame
import os
from subprocess import Popen


class Graphics:
    def __init__(self):
        self.done = False
        pygame.init()
        self.display = pygame.display
        self.scr_w = self.display.Info().current_w
        self.scr_h = self.display.Info().current_h
        self.screen = self.display.set_mode(size=[self.scr_w, self.scr_h])  # , flags=pygame.FULLSCREEN, display=0)
        self.screen.fill([0, 0, 0])
        print(pygame.image.get_extended())
        self.path = "videos/1080_60fps.mp4"



    def load_image(self, image_path=os.path.join('images', 'room_0', 'wall_0', '0.png')):
        try:
            img = pygame.image.load(image_path)
            self.screen.blit(img, [0, 0])
            if '0.png' in image_path:
                omxc = Popen(['omxplayer', '-b', self.path])
            else:
                os.system('killall omxplayer.bin')
            pygame.display.flip()
        except:
            pass

        self.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                break


# g = Graphics()
# while 1:
#     g.load_image()
