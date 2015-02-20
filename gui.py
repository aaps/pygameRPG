import pygame
from funciones import *
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
        self.movement = (0, 0)
    def update(self):
        (self.left,self.top) = pygame.mouse.get_pos()
        self.movement = pygame.mouse.get_rel()

class Button(pygame.sprite.Sprite):
    def __init__(self, img1, img2, img3, text=None, size=12, color=(1,1,1), x=40, y=40, OnClick=None):
        self.img_n = load_image(img1, alpha=1)
        self.img_s = load_image(img2, alpha=1)
        self.img_c = load_image(img3, alpha=1)
        self.rect = self.img_n.get_rect()
        (self.rect.left, self.rect.top) = (x, y)
        self.T = False
        if text != None:
            self.text = fuente(t=size).render(text, True, color)
            self.textrect = self.text.get_rect()
            self.textrect.center = self.rect.center
            self.T = True
        self.img_actual = self.img_n
        self.activado = False
        self.OnClick = OnClick
    def collide(self, cursor):
        if cursor != 1:
            if  cursor.colliderect(self.rect):
                self.activado = True
                return True
        else:
            if self.activado:
                self.activado = False
                return self.OnClick
            self.activado = False
            return 0
            
    def Move(self, move):
        self.rect.move_ip(move)
        if self.T:
            self.textrect.move_ip(move)
    def update(self, screen, cursor,):
        if self.activado:
            self.img_actual = self.img_c
        elif cursor.colliderect(self.rect):
            self.img_actual = self.img_s
        else:
            self.img_actual = self.img_n
        screen.blit(self.img_actual,self.rect)
        if self.T:
            screen.blit(self.text,self.textrect)
class CheckButton(pygame.sprite.Sprite):
    def __init__(self, x=10, y=10):
        self.b_uncheck = load_image("check_button1.png", 1)
        self.b_check = load_image("check_button2.png", 1)
        self.b_image = self.b_uncheck
        self.rect = self.b_image.get_rect()
        (self.rect.left, self.rect.top) = (x, y)
        self.check = False
    def collide(self, cursor):
        if cursor.colliderect(self.rect):
            if self.check:
                self.check = False
                self.b_image = self.b_uncheck
            else:
                self.check = True
                self.b_image = self.b_check
            return True
        return False
        
    def Move(self, move):
        self.rect.move_ip(move)
    def update(self, screen, cursor):
        screen.blit(self.b_image, self.rect)
class Text(pygame.sprite.Sprite):
    def __init__(self, text, size=12, color=(255,255,255), left=0, top=0, font=None):
        self.text = fuente(font=font, t=size).render(text, True, color)
        self.rect = self.text.get_rect()
        (self.rect.left, self.rect.top) = (left, top)
    def Move(self, move):
        self.rect.move_ip(move)
    def update(self, screen):
        screen.blit(self.text, self.rect)
        
class Menu(pygame.sprite.Sprite):
    def __init__(self, text, size=12, color=(1,1,1), x=0, y=0, buttons=0):
        self.menu = [Button('menu1.png',
                        'menu2.png',
                        'menu3.png',
                        text=text, size=size, color=color, x=x, y=y)]
        for i in range(buttons):
            self.menu.append(Button('menu1.png',
                        'menu2.png',
                        'menu3.png',
                        text="Boton"+str(i+1), size=size, color=color, x=x, y=(i+1)*self.menu[0].rect.h+y))
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.open = False
        
    def Move(self, move):
        for i in range(len(self.menu)):
            self.menu[i].Move(move)    
    def update(self, screen, cursor):
        if self.open:
            for button in self.menu:
                button.update(screen, cursor)
        else:
            self.menu[0].update(screen, cursor)
    def collide(self, cursor):
        if cursor != 1:
            for i in range(len(self.menu)):
                if cursor.colliderect(self.menu[i].rect):
                    if i == 0:
                        if self.open:
                            self.open = False
                            return True
                        else:
                            self.open = True
                            return True
                    else:
                        self.menu[i].activado = True
                        return True
            self.open = False
            return False
        else:
            for i in range(len(self.menu)):
                self.menu[i].activado = False
    def rename(self, L):
        for i in range(len(self.menu)):
            if L[i] != "":
                text = fuente(self.size).render(L[i], True, self.color)
                textrect = text.get_rect()
                textrect.center = self.menu[i].rect.center
                (self.menu[i].text, self.menu[i].textrect) = (text, textrect)
                
class Window:
    def __init__(self, width=300, height=300, left=40, top=40, moveable=False):
        self.window = pygame.Surface((width, height))
        self.rect = self.window.get_rect()
        (self.rect.left, self.rect.top) = (left, top)
        self.buttons = []
        self.checkbuttons = []
        self.menus = []
        self.images = []
        self.bgimages = []
        self.texts = []
        self.objects = []
        self.receptors = []
        self.entrys = []
        self.move_available = moveable
        self.moveable = False
        
    def appendButton(self, b):
        self.buttons.append(b)
        self.buttons[len(self.buttons)-1].rect.left += self.rect.left
        self.buttons[len(self.buttons)-1].rect.top += self.rect.top
        if b.T:
            self.buttons[len(self.buttons)-1].textrect.left += self.rect.left
            self.buttons[len(self.buttons)-1].textrect.top += self.rect.top
    def appendCheckButton(self, cb):
        self.checkbuttons.append(cb)
    def appendMenu(self, m):
        self.menus.append(m)
        for c in range(len(self.menus[len(self.menus)-1].menu)):
            self.menus[len(self.menus)-1].menu[c].rect.left += self.rect.left
            self.menus[len(self.menus)-1].menu[c].rect.top += self.rect.top
            self.menus[len(self.menus)-1].menu[c].textrect.left += self.rect.left
            self.menus[len(self.menus)-1].menu[c].textrect.top += self.rect.top
    
    def appendImage(self, img):
        self.images.append(img)
        self.images[len(self.images)-1].rect.left += self.rect.left
        self.images[len(self.images)-1].rect.top += self.rect.top
    def appendBGImage(self, img):
        (img.rect.left, img.rect.top) = (img.rect.left+self.rect.left, img.rect.top+self.rect.top)
        self.bgimages.append(img)
        
    def appendText(self, text):
        text.rect.left += self.rect.left
        text.rect.top += self.rect.top
        self.texts.append(text)
    def appendObject(self, obj):
        obj.rect.left += self.rect.left
        obj.rect.top += self.rect.top
        obj.last_rect_center = obj.rect.center
        self.objects.append(obj)
    def appendReceptor(self, rec):
        rec.rect.left += self.rect.left
        rec.rect.top += self.rect.top
        self.receptors.append(rec)
    def appendTextEntry(self, entry):
        entry.RectOutLine.left += self.rect.left
        entry.RectOutLine.top += self.rect.top
        entry.RectEntry.left += self.rect.left
        entry.RectEntry.top += self.rect.top
        entry.CursorLine.left += self.rect.left
        entry.CursorLine.top += self.rect.top
        self.entrys.append(entry)
    def collide(self, cursor):
        if cursor != 1:
            for i in range(len(self.objects)):
                if self.objects[i].collide(cursor):
                    return 0
            for i in range(len(self.menus)):
                if self.menus[i].collide(cursor):
                    return 0
            for i in range(len(self.buttons)):
                if self.buttons[i].collide(cursor):
                    return True
            for i in range(len(self.checkbuttons)):
                if self.checkbuttons[i].collide(cursor):
                    return 0
            for i in range(len(self.entrys)):
                if self.entrys[i].collide(cursor):
                    pass
            if self.rect.colliderect(cursor):
                self.moveable = True
        else:
            for i in range(len(self.objects)):
                obj = self.objects[i].collide(1)
                if obj:
                    x=0
                    for c in range(len(self.receptors)):
                        if self.objects[i].rect.colliderect(self.receptors[c].rect) and self.receptors[c].state==False:
                            self.objects[c] = self.objects[i]
                            self.objects[c].rect.center = self.receptors[c].rect.center
                            self.objects[i] = Object()
                            self.receptors[i].state = False 
                            self.receptors[c].state = True
                            x=1
                            break
                    if not x:
                        self.objects[i].rect.center = self.objects[i].last_rect_center
                    break
            for i in range(len(self.menus)):
                self.menus[i].collide(1)
            for i in range(len(self.buttons)):
                OnClick = self.buttons[i].collide(1)
                if OnClick != 0:
                    return OnClick
            self.moveable = False
            
    def Move(self, move):
        self.rect.move_ip(move)
        for i in range(len(self.buttons)):
            self.buttons[i].Move(move)
        for i in range(len(self.menus)):
            self.menus[i].Move(move)
        for i in range(len(self.checkbuttons)):
            self.checkbuttons[i].Move(move)
        for i in range(len(self.images)):
            self.images[i].Move(move)
        for i in range(len(self.bgimages)):
            self.bgimages[i].Move(move)
        for i in range(len(self.texts)):
            self.texts[i].Move(move)
        for i in range(len(self.objects)):
            self.objects[i].Move(move)
        for i in range(len(self.receptors)):
            self.receptors[i].Move(move)
        for i in range(len(self.entrys)):
            self.entrys[i].Move(move)

    def update(self, screen, cursor):
        if self.move_available:
            move = cursor.movement
            if self.moveable:
                self.Move(move)
        self.window.fill([255,255,255])
        #pygame.draw.rect(screen, (0,0,200), self.rect, 2)
        for bg in self.bgimages:
            bg.update(screen)
        for b in self.buttons:
            b.update(screen, cursor)
        for cb in self.checkbuttons:
            cb.update(screen, cursor)
        for m in self.menus:
            m.update(screen, cursor)
        for i in self.images:
            i.update(screen)
        #for r in self.receptors:
        #    r.update(screen)
        for t in self.texts:
            t.update(screen)
        for o in self.objects:
            o.update(screen, cursor)
        for e in self.entrys:
            e.update(screen)
            
    def EntryEvents(self, event, keys):
        for i in range(len(self.entrys)):
            if self.entrys[i].Write:
                self.entrys[i].TapKey(event, keys)
class Image:
    def __init__(self, image, left=0, top=0):
        self.image = load_image(image, True, alpha=1)
        self.rect = self.image.get_rect()
        (self.rect.left, self.rect.top) = (left, top)
    def Move(self, move):
        self.rect.move_ip(move)
    def update(self, screen):
        screen.blit(self.image, self.rect)
    def ChangeImage(self, surface):
        self.image = surface
        (left, top) = (self.rect.left, self.rect.top)
        self.rect = self.image.get_rect()
        (self.rect.left, self.rect.top) = (left, top)
class Object:
    def __init__(self, Type=None, image=None, left=0, top=0, width=0, height=0, moveable=False, reference=None):
        self.Type = Type
        self.image = image
        self.reference = reference
        self.rect = pygame.Rect([left, top, width, height])
        self.moveable = moveable
        self.move_available = False
        self.last_rect_center = self.rect.center
    def update(self, screen, cursor):
        if self.moveable and self.move_available:
            move = cursor.movement
            self.Move(move)
        if self.image != None:
            screen.blit(self.image, self.rect)
        else:
            pass
            #pygame.draw.rect(screen, (0,0,100), self.rect, 2)
    def Move(self, move):
        self.rect.move_ip(move)
    def collide(self, cursor):
        if cursor != 1:
            if cursor.colliderect(self.rect):
                if self.moveable:
                    self.move_available = True
                    self.last_rect_center = self.rect.center
                    self.rect.center = cursor.center
        else:
            if self.move_available:
                #self.rect.center = self.last_rect_center
                self.move_available = False
                return True
            self.move_available = False
            return False
            
class Receptor:
    def __init__(self, Type=None, left=0, top=0, width=0, height=0):
        self.ReceptType = Type
        self.state = False
        rect = pygame.Rect([left, top, width, height])
        self.rect = pygame.Rect([left, top, 12, 12])
        self.rect.center = rect.center
        
    def update(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        
    def Move(self, move):
        self.rect.move_ip(move)
        
class TextEntry:
    def __init__(self, password=False, left=0, top=0, width=0, height=0):
        self.RectOutLine = pygame.Rect([left, top], [width+4, height+4])
        self.RectEntry = pygame.Rect([left+2, top+2], [width, height])
        self.TextEntry = ""
        self.TextSurface = Text(self.TextEntry)
        self.TextSurface.rect.centery = self.RectEntry.centery
        self.TextSurface.rect.left = self.RectEntry.left+3
        self.CursorLine = pygame.Rect([0, 0], [2, height-2])
        self.CursorLine.centery = self.RectEntry.centery
        self.CursorLine.left = self.TextSurface.rect.right
        self.Password = password
        self.Write = False
        self.Timer = 0
        
    def update(self, screen):
        pygame.draw.rect(screen, (52,52,52), self.RectOutLine)
        pygame.draw.rect(screen, (220,220,220), self.RectEntry)
        if self.Write:
            if self.Timer >= 15:
                pygame.draw.rect(screen, (52,52,52), self.CursorLine)
        self.TextSurface.update(screen)
        self.Timer +=0.5
        if self.Timer == 30:
            self.Timer = 0
        
        
    def collide(self, cursor):
        if cursor.colliderect(self.RectEntry):
            self.Write = True
            return True
        else:
            self.Write = False
        
    def Move(self, move):
        self.RectOutLine.move_ip(move)
        self.RectEntry.move_ip(move)
        self.CursorLine.move_ip(move)
        self.TextSurface.Move(move)
        
    def TapKey(self, event, keys):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.TextEntry = self.TextEntry[:-1]
            elif len(self.TextEntry) >= 15:
                return False
            elif event.key == pygame.K_a:
                self.TextEntry += "a"
            elif event.key == pygame.K_b:
                self.TextEntry += "b"
            elif event.key == pygame.K_c:
                self.TextEntry += "c"
            elif event.key == pygame.K_d:
                self.TextEntry += "d"
            elif event.key == pygame.K_e:
                self.TextEntry += "e"
            elif event.key == pygame.K_f:
                self.TextEntry += "f"
            elif event.key == pygame.K_g:
                self.TextEntry += "g"
            elif event.key == pygame.K_h:
                self.TextEntry += "h"
            elif event.key == pygame.K_i:
                self.TextEntry += "i"
            elif event.key == pygame.K_j:
                self.TextEntry += "j"
            elif event.key == pygame.K_k:
                self.TextEntry += "k"
            elif event.key == pygame.K_l:
                self.TextEntry += "l"
            elif event.key == pygame.K_m:
                self.TextEntry += "m"
            elif event.key == pygame.K_n:
                self.TextEntry += "n"
            elif event.key == pygame.K_o:
                self.TextEntry += "o"
            elif event.key == pygame.K_p:
                self.TextEntry += "p"
            elif event.key == pygame.K_q:
                self.TextEntry += "q"
            elif event.key == pygame.K_r:
                self.TextEntry += "r"
            elif event.key == pygame.K_s:
                self.TextEntry += "s"
            elif event.key == pygame.K_t:
                self.TextEntry += "t"
            elif event.key == pygame.K_u:
                self.TextEntry += "u"
            elif event.key == pygame.K_v:
                self.TextEntry += "v"
            elif event.key == pygame.K_w:
                self.TextEntry += "w"
            elif event.key == pygame.K_x:
                self.TextEntry += "x"
            elif event.key == pygame.K_y:
                self.TextEntry += "y"
            elif event.key == pygame.K_z:
                self.TextEntry += "z"
            elif event.key == pygame.K_0 or event.key == pygame.K_KP0:
                self.TextEntry += "0"
            elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                self.TextEntry += "1"
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                self.TextEntry += "2"
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                self.TextEntry += "3"
            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                self.TextEntry += "4"
            elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                self.TextEntry += "5"
            elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                self.TextEntry += "6"
            elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                self.TextEntry += "7"
            elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                self.TextEntry += "8"
            elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                self.TextEntry += "9"
            elif event.key == 47 and (keys[K_LSHIFT] or keys[K_RSHIFT]):
                self.TextEntry += "_"
            else:
                return 0
        if self.Password:
            self.TextSurface = Text(len(self.TextEntry)*"*", color=(20,20,20), size=16, font="Candara")
        else:
            self.TextSurface = Text(self.TextEntry, color=(20,20,20), size=16, font="Candara")
        self.TextSurface.rect.centery = self.RectEntry.centery
        self.TextSurface.rect.left = self.RectEntry.left+3
        
        self.CursorLine.left = self.TextSurface.rect.right
        
    def GetText(self):
        return self.TextEntry
        
        
            