import pygame
import os
from PIL import Image


class Graphics:
    def __init__(self):
        self.done = False
        pygame.init()
        self.display = pygame.display
        self.scr_w = self.display.Info().current_w
        self.scr_h = self.display.Info().current_h
        self.screen = self.display.set_mode(size=[self.scr_w, self.scr_h])#, flags=pygame.FULLSCREEN, display=0)
        self.screen.fill([0, 0, 0])
        print(pygame.image.get_extended())

    def load_image(self, image_path=os.path.join('images', 'room_0', 'wall_0', '1.png')):
        # try:
        #     img = pygame.image.load(image_path)
        # except:
        #     f = Image.open(image_path)
        #     f = f.save(os.path.join('images', '{}.bmp'.format(image_num)))
        #     img = pygame.image.load(os.path.join('images', '{}.bmp'.format(image_num)))
        img = pygame.image.load(image_path)
        self.screen.blit(img, [0, 0])
        self.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                break
