#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import random
from funciones import *
from engine import HEIGHT,WIDTH
pygame.init()

class SpriteMap( pygame.sprite.Sprite ):
    def __init__(self,imagen=None, rect=None):
        pygame.sprite.Sprite.__init__( self )
        self.imagen = imagen
        self.rect = rect
    def update(self,screen,vx,vy):
        self.rect.move_ip(-vx,-vy)
        if self.imagen != None:
            screen.blit(self.imagen,self.rect)

class Personaje(pygame.sprite.Sprite):
    def __init__(self,speed,w,h):
        pygame.sprite.Sprite.__init__( self )
        self.chara = cortar_chara("graphics/charasets/char.png", 4, 4)
        self.image = self.chara[0][0]
        
        self.rectd = self.image.get_rect()
        self.rectd.left = w/2-self.rectd.w/2
        self.rectd.top = h/2-self.rectd.h/2
        
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-5,-30)
        self.rect.center = (w/2, h/2+14)
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.vLEFT,self.vRIGHT,self.vUP,self.vDOWN=False,False,False,False
        
        self.Spell = None
        self.SpellRing = pygame.Rect([0,0],[30,30])
        self.SpellRing.centerx = self.rectd.centerx
        self.SpellRing.centery = self.rectd.centery+18
        self.SpellRingTimerColor = 0
        self.SpellRingColors = [(249,204,133),(249,237,133),(212,249,133),(168,249,133),(212,249,133),(249,237,133)]
        self.UsingSpell = False
        self.StartSpell = False
        self.Spellvx = 0
        self.Spellvy = 0
        self.CastingTime = 0
        self.SpellReady = False
        
        self.SpellCastRect = pygame.Rect((0,0),(30,5))
        self.SpellCurrenCast = pygame.Rect((0,0),(28,3))
        self.SpellCastRect.centerx = self.rect.centerx
        self.SpellCastRect.top = self.rect.bottom+7
        self.SpellCurrenCast.left = self.SpellCastRect.left+1
        self.SpellCurrenCast.top = self.SpellCastRect.top+1
        
        self.maxhprect = pygame.Rect((0, 0), (30, 5))
        self.hprect = pygame.Rect((0, 0), (28, 3))
        self.maxhprect.centerx = self.rect.centerx
        self.maxhprect.top = self.rect.bottom+3
        self.hprect.left = self.maxhprect.left+1
        self.hprect.top = self.maxhprect.top+1
        
        # Atributos del Personaje
        self.nombre = None
        self.especializacion = "Aventurero"
        self.nivel = 1
        self.str = 1;self.str_b = 0
        self.int = 1;self.int_b = 0
        self.agi = 1;self.agi_b = 0
        self.dex = 1;self.dex_b = 0
        self.vit = 1;self.vit_b = 0
        self.stat_points = 5
        self.soul_points = 0
        self.stone_points = 0
        self.atack = 10;self.atack_b = 0
        self.defense = 5;self.defense_b = 0
        self.dodge = 8;self.dodge_b = 0
        self.crit = 3;self.crit_b = 0
        self.maxhp = 50;self.maxhp_b = 0
        self.hp = self.maxhp
        self.maxsp = 15;self.maxsp_b = 0
        self.sp = self.maxsp
        self.exp = 0
        self.exp_nivel = 100
        self.cash = 100
        self.bag = []
        for i in range(30):
            self.bag.append(None)
        self.Equipo()
# Equipo [1-BODY,2-R,3-HEAD,4-GLOBE,5-LEGS,6-SHOES,7-RING1,8-RING2,9-NECKLACE]
    def Equipo(self):
        self.equip = [] 
        for i in range(9):
            self.equip.append(None)
        
    def HpBarsUpdate(self, screen):
        pygame.draw.rect(screen, (52,52,52), self.maxhprect)
        pygame.draw.rect(screen, (215,94,56), self.hprect)
        
    def update(self, screen, t):
        if not self.UsingSpell:
            self.dir = self.mover(t)
            if self.Spell != None:
                if self.Spell.Delete:
                    self.DeleteSpell()
        else:
            self.MoveSpellRing()
            self.SpellRing.move_ip(self.Spellvx, self.Spellvy)
            self.Spell.Rect.center = self.SpellRing.center
            self.SpellCurrenCast.width = self.CastingTime*28.0/self.Spell.CastTime
            if self.CastingTime >= self.Spell.CastTime:
                self.SpellReady = True
            else:
                self.CastingTime += 0.025
        screen.blit(self.dir, self.rectd)
        self.HpBarsUpdate(screen)
        if self.UsingSpell:
            pygame.draw.rect(screen, (52,52,52),self.SpellCastRect)
            pygame.draw.rect(screen, (102,204,255),self.SpellCurrenCast)
            
        if self.SpellRingTimerColor == 59:
            self.SpellRingTimerColor = 0
        self.SpellRingTimerColor +=0.5
        #pygame.draw.rect(screen,(200,1,105),self.rectcol)
        #pygame.draw.rect(screen, (255,255,255), self.rect)

    def MoveSpellRing(self):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.Spellvx = 1.5
        if keys[K_LEFT]:
            self.Spellvx = -1.5
        if keys[K_DOWN]:
            self.Spellvy = 1.5
        if keys[K_UP]:
            self.Spellvy = -1.5
        if not ( keys[K_RIGHT] or keys[K_LEFT]):
            self.Spellvx = 0
        if not (keys[K_DOWN] or keys[K_UP] ):
            self.Spellvy = 0
    def mover(self, t):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.vx = self.speed
            self.x = 2
            self.image = self.chara[2][0]
        if keys[K_LEFT]:
            self.vx = -self.speed
            self.x = 1
            self.image = self.chara[1][0]
        if keys[K_DOWN]:
            self.vy = self.speed
            self.x = 0
            self.image = self.chara[0][0]
        if keys[K_UP]:
            self.vy = -self.speed
            self.x = 3
            self.image = self.chara[3][0]
        if not ( keys[K_RIGHT] or keys[K_LEFT] or keys[K_DOWN] or keys[K_UP] ):
            self.vx = 0; self.vy = 0
        if self.vx != 0 and self.vy != 0 :
            self.vy = 0
        if self.vx==0 and self.vy==0:
            return self.image
        return self.chara[self.x][t/10-1]
    
    def atacar(self, moblist, spell=False, massive=False):
        for i in range(len(moblist)):
            if not spell:
                if self.rect.colliderect(moblist[i].rect):
                    return i+1
            else:
                if self.SpellRing.colliderect(moblist[i].rect):
                    return i+1
        return False
    
    def UseSpell(self):
        self.UsingSpell = True
        self.vx = 0
        self.vy = 0
        self.dir = self.chara[self.x][0]
    def DeleteSpell(self):
        self.SpellRing.centerx = self.rectd.centerx
        self.SpellRing.centery = self.rectd.centery+18
        self.UsingSpell = False
        self.Spellvx = 0
        self.Spellvy = 0
        self.CastingTime = 0
        self.SpellReady = False
        self.StartSpell = False
        self.Spell = None
    def dano(self):
        return random.randint(self.atack/2,self.atack)
    def SpellRingUpdate(self, screen):
        color = self.SpellRingColors[int(self.SpellRingTimerColor)/10]
        pygame.draw.ellipse(screen,color,self.SpellRing, 3)
    
    def SubirNivel(self):
        self.nivel += 1
        self.stat_points += 5
        self.atack +=4
        self.defense += 2
        self.maxhp += self.nivel*6
        self.hp = self.maxhp
        self.maxsp += self.nivel*2-2
        self.sp = self.maxsp
        self.exp = self.exp-self.exp_nivel
        self.exp_nivel = self.exp_nivel*3/2
class Mounstro( pygame.sprite.Sprite):
    def __init__(self, (expresion, x, y),(xj,yj)):
        pygame.sprite.Sprite.__init__( self )
        M = self.traductor(expresion)
        self.nombre = M[0]
        self.tipo = M[1]
        self.nivel = int(M[2])
        self.maxhp = int(M[3])
        self.hp = self.maxhp
        self.maxsp = int(M[4])
        self.sp = self.maxsp
        self.exp = int(M[5])
        self.atack = int(M[6])
        self.defense = int(M[7])
        self.drops = M[8]
        self.movimiento = int(M[9])
        self.HAB1 = M[10]
        self.HAB2 = M[11]
        self.HAB3 = M[12]
        self.HAB4 = M[13]
        self.sprite = cortar_chara("graphics/mobs/"+M[15], 4, 4)
        self.image = self.sprite[0][0]
        self.rect = self.image.get_rect()
        self.rect.left = x-xj+WIDTH/2
        self.rect.top = y-yj+HEIGHT/2
        
        self.maxhprect = pygame.Rect((0, 0), (30, 5))
        self.hprect = pygame.Rect((0, 0), (28, 3))
        self.maxhprect.centerx = self.rect.centerx
        self.maxhprect.top = self.rect.bottom+3
        self.hprect.left = self.maxhprect.left+1
        self.hprect.top = self.maxhprect.top+1
        
        self.caminar = False
        self.vx = 0
        self.vy = 0
    def traductor(self,exp):
        exp = exp.split("_")
        mobDB = open("MobDataBase.txt")
        for line in mobDB:
            
            if line[0]!="#":
                Variables = line.strip().split(",")
                
                if Variables[1]==exp[0] and Variables[2]==exp[1]:
                        return Variables
    def update(self, screen, j, time, hubo_colision, col):
        a = random.randint(1,400)
        if a <=9 :
            self.caminar = False
            self.vx, self.vy = 0, 0
        elif a == 400:
            self.caminar = True
            orientacion = random.choice(["x","y"])
            direccion = random.choice([-2,2])
            if orientacion == "x":
                self.vy = 0
                self.vx = direccion
            elif orientacion == "y":
                self.vx = 0
                self.vy = direccion 
            if self.vx == -2:
                self.nSprite = 1
                self.image = self.sprite[1][0]
            elif self.vx:
                self.nSprite = 2
                self.image = self.sprite[2][0]
            elif self.vy == -2:
                self.nSprite = 3
                self.image = self.sprite[3][0]
            else:
                self.nSprite = 0
                self.image = self.sprite[0][0]
        if not col:
            self.oldleft = self.rect.left
            self.oldtop = self.rect.top
        else:
            self.oldleft -= j.vx
            self.oldtop -= j.vy
            self.rect.left = self.oldleft
            self.rect.top = self.oldtop
            self.vx = 0
            self.vy = 0
        self.maxhprect.centerx = self.rect.centerx
        self.maxhprect.top = self.rect.bottom+3
        if self.caminar:
            if hubo_colision:
                self.rect.move_ip(self.vx, self.vy)
                self.maxhprect.move_ip(self.vx, self.vy)
                self.hprect.centery = self.maxhprect.centery
                self.hprect.left = self.maxhprect.left+1
                screen.blit(self.sprite[self.nSprite][time/10-1], self.rect)
            else:
                self.rect.move_ip(-j.vx + self.vx, -j.vy + self.vy)
                self.maxhprect.move_ip(-j.vx +self.vx, -j.vy + self.vy)
                self.hprect.centery = self.maxhprect.centery
                self.hprect.left = self.maxhprect.left+1
                screen.blit(self.sprite[self.nSprite][time/10-1], self.rect)
        else:
            if hubo_colision:
                #self.rect.move_ip(-j.vx,-j.vy)
                screen.blit(self.image,self.rect)   
            else:
                self.rect.move_ip(-j.vx,-j.vy)
                self.maxhprect.move_ip(-j.vx,-j.vy)
                self.hprect.centery = self.maxhprect.centery
                self.hprect.left = self.maxhprect.left+1
                screen.blit(self.image,self.rect)
    def HpBarsUpdate(self, screen):
        pygame.draw.rect(screen, (111,0,0), self.maxhprect)
        pygame.draw.rect(screen, (215,94,56), self.hprect)
        
class Item:
    def __init__(self, ID, rect=None):
        self.ID = ID
        item = self.CargarItem()
        self.tipo = item[1]
        self.nombre = item[2]
        self.atack = int(item[3])
        self.defense = int(item[4])
        self.maxhp = int(item[5])
        self.maxsp = int(item[6])
        self.nivel = item[7]
        self.cant = int(item[8])
        self.fx = item[9]
        self.image_inv = load_image("graphics/item/"+item[10][:-1]+"a.gif", alpha = 1)
        self.image_des = "graphics/item/"+item[10][:-1]+"b.gif"
        self.rect_inv = rect
        self.moveable = False
    def CargarItem(self):
        ItemDB = open("ItemDataBase.txt", "r")
        for item in ItemDB:
            i = item.split('\t')
            if str(i[0]) == str(self.ID):
                return i
    def update(self, screen, image, j, hubo_colision):
        if not hubo_colision:
            self.rect_inv.move_ip(-j.vx, -j.vy)
        screen.blit(image, self.rect_inv)
        
            
