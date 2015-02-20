import time
import pygame
from pygame.locals import *
pygame.mixer.init()
pygame.mixer.music.load('Dungeon1.ogg')
pygame.mixer.music.play(loops=-1)
time.sleep(20)
pygame.mixer.music.fadeout(5000)
pygame.mixer.music.load('Theme1.ogg')
pygame.mixer.music.play(loops=-1)
time.sleep(5)
pygame.mixer.music.fadeout(5000)
