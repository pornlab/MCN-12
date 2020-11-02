if __name__ == "__main__":
    import os
    import time

    try:
        #os.system('pip3 install -U pygame==2.0.0.dev12')
        import pygame
    except:

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
