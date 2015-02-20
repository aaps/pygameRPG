import pygame, sys
from pygame.locals import *
from funciones import *

class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def update(self):
        (self.left,self.top) = pygame.mouse.get_pos()

class Boton(pygame.sprite.Sprite):
    def __init__(self, img1, img2, x=40, y=40):
        self.img_n = load_image(img1, 1)
        self.img_s = load_image(img2, 1)
        self.img_actual = self.img_n
        self.activado = 0
        self.rect = self.img_actual.get_rect()
        (self.rect.top, self.rect.left) = (y, x)
    def update(self, screen, cursor):
        if  cursor.colliderect(self.rect):
            self.img_actual = self.img_s
        else:
            self.img_actual = self.img_n
        screen.blit(self.img_actual,self.rect)
    def color(self, event, cfondo, color, cursor):
        if event.type == pygame.MOUSEBUTTONDOWN and cursor.colliderect(self.rect):
            if not self.activado:
                self.activado = 1
            else:
                self.activado = 0
        if self.activado:
            return color
        else: return cfondo
def main():
    screen = pygame.display.set_mode([640,480])
    pygame.display.set_caption("Botones Pygame")
    blanco = (255,255,255)
    rojo = (200,0,0)
    cursor = Cursor()
    boton = Boton("rojo1.png", "rojo2.png", 200, 200)
    clock = pygame.time.Clock()
    
    wea = Contructor('graphics/c_0.png', 'graphics/c_1.png', 300, 50, (65,65,65))
    wea_rect = wea.get_rect()
    wea_rect.left = 100
    wea_rect.top=100
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit() 
            color_actual = boton.color(event, blanco, rojo, cursor)
        clock.tick(60)
        screen.fill(color_actual)
        
        
        cursor.update()
        boton.update(screen, cursor)
        screen.blit(wea, wea_rect)
        pygame.display.update()
        
main()