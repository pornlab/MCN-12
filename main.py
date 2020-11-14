if __name__ == "__main__":
    import os
    import time

    try:
        import pygame
    finally:
        os.system('pip3 install -U pygame==1.9.6')
        import pygame

    try:
        import RPi.GPIO as IO
    finally:
        os.system('pip3 install RPi.GPIO')
        import RPi.GPIO as IO

    try:
        import moviepy
    finally:
        os.system('pip3 install moviepy==1.0.3')
        import pyglet

    try:
        import ctypes
    finally:
        os.system('pip3 install ctypes')
        import ctypes

    time.sleep(1)
    cmd = os.system('git -C "/home/pi/MCN-12" pull origin master')
    time.sleep(5)

    from routine import Routine
    r = Routine()
