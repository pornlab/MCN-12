if __name__ == "__main__":
    import os
    import time

    try:
        import pygame
    except:
        os.system('sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev '
                  'libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev '
                  'libavformat-dev libavcodec-dev libfreetype6-dev')
        os.system('pip3 install -U pygame==1.9.2')
        import pygame

    try:
        import RPi.GPIO as IO
    except:
        os.system('pip3 install RPi.GPIO')
        import RPi.GPIO as IO

    time.sleep(1)
    cmd = os.system('git -C "/home/pi/MCN-12" pull origin master')
    time.sleep(5)

    from routine import Routine
    r = Routine()
