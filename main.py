if __name__ == "__main__":
    import os
    import time
    try:
        import pygame
    except:
        os.system('pip3 install pygame')
    time.sleep(1)
    cmd = os.system('git -C "/home/pi/MCN-12" pull origin master')
    time.sleep(5)

    from routine import Routine
    r = Routine()
    r.start()
