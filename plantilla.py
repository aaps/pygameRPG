'''
Created on 25-07-2012

@author: Ednar
'''
import pygame, sys
from gui import *
from pygame.locals import *
from funciones import *

def main():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    clock = pygame.time.Clock()
    cursor = Cursor()
    b1 = Button("graphics/button_1.png", "graphics/button_2.png", "graphics/button_3.png", text="?", size=18, color=(1,1,1), x=100 ,y=0)
    b2 = Button("graphics/button_1.png", "graphics/button_2.png", "graphics/button_3.png", text="H", size=18, color=(1,1,1), x=130 ,y=0)
    win = Window(width=500, height=27, left=150, top=10, moveable=True)
    menu1 = Menu(text="Menu1", size=14, color=(1,1,1), buttons=6, x=0, y=3)
    menu1.rename(["Actions", "Act 1", "Act 2", "Act 3", "Act 4", "Act 5", "Act 6"])
    win.appendMenu(menu1)
    win.appendButton(b1)
    win.appendButton(b2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    win.collide(cursor)
            if event.type == pygame.MOUSEBUTTONUP:
                win.collide(1)
        screen.fill((0,0,0))
        cursor.update()
        win.update(screen, cursor)
        clock.tick(60)
        pygame.display.update()
main()