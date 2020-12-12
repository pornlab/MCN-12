import pygame
import os
import sys
import threading
from subprocess import Popen


class Graphics:
    def __init__(self):
        self.done = False
        pygame.init()
        self.display = pygame.display
        self.video_playing = False
        self.scr_w = self.display.Info().current_w
        self.scr_h = self.display.Info().current_h
        self.screen = self.display.set_mode(size=[self.scr_w, self.scr_h])  # , flags=pygame.FULLSCREEN, display=0)
        self.screen.fill([0, 0, 0])
        print(pygame.image.get_extended())
        self.path_1 = "videos/1080_60fps.mp4"
        self.path_2 = "videos/button.mp4"


    def load_image(self, image_path=os.path.join('images', 'room_0', 'wall_0', '0.png')):
        try:
            if image_path != os.path.join('images', 'room_5'):
                img = pygame.image.load(image_path)
            print('in function...', image_path)
            if image_path == os.path.join('images', 'room_5'):
                if self.video_playing:
                    x = threading.Thread(target=os.system, args=('killall omxplayer.bin', ))
                    x.start()
                    #os.system('killall omxplayer.bin')
                    self.video_playing = False
                omxc = Popen(['omxplayer', '-o',  'local', self.path_2])
                img = None
            elif image_path == os.path.join('images', 'room_0', 'wall_0', '0.png'):
                if not self.video_playing:
                    omxc = Popen(['omxplayer', '-o',  'local', '--loop', self.path_1])
                    self.video_playing = True
                img = None
            else:
                os.system('killall omxplayer.bin')
                self.video_playing = False

            self.screen.blit(img, [0, 0])
            pygame.display.flip()
        except:
            pass

        self.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.system('killall omxplayer.bin')
                self.video_playing = False
                pygame.quit()
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                os.system('killall omxplayer.bin')
                self.video_playing = False
                pygame.quit()
                return True
        return False
