#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------
# Módulos
import sys, pygame
import random
from pygame.locals import *
from interfaz import *
from maps import *
from funciones import *
from engine import WIDTH, HEIGHT, velocidad
# ------------------------------------------------------------------------------------
# Constantes
#WIDTH = 800
#HEIGHT = 600
#velocidad = 2
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
class RPG:
    def __init__(self):
        # Inicializacion y pantalla
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Land of Mistery | ver Alpha - 2012")
        
        # Interfaz, Mapa y Jugador
        
        self.I = InterfazJuego(self.screen)
        self.PlayerGroup = pygame.sprite.RenderUpdates(self.I.jugador)
        
        self.MapTest = Mapa("mapa1.tmx")
        self.cursor = Cursor()
        self.DroppedItems = []
        
        #Ventanas activas
        self.bag_act = False
        self.runes_act = False
        self.char_act = False
        self.equip_act = False
        self.MobBar_act = False
        
        #Manejo de delay y tiempo
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delayAtk = 0
        
        #Musica
        pygame.mixer.init()
        
        self.bucle_partida()
        self.bucle_principal()
    def bucle_principal(self):
        pygame.mixer.music.load('music/village2.mid')
        pygame.mixer.music.play(loops=-1)
        while True:
            self.screen.fill((0,0,0))
            self.Hotkeys()
            self.clock.tick(60)
            self.time+=1
            self.delayAtk+=1
            
            if self.time>40:
                self.time=0
                
            self.cursor.update()
            hubo_colision = pygame.sprite.spritecollideany(self.I.jugador, self.MapTest.colisionesGroup)
            
            self.MapTest.update(self.screen, self.I.jugador, hubo_colision)
            
            self.I.jugador.SpellRingUpdate(self.screen)
            self.MapTest.MobsUpdate(self.screen, self.I.jugador, self.time, hubo_colision) 
            self.ItemDropUpdate(hubo_colision)
            self.I.jugador.update(self.screen, self.time)
            self.screen.blit(self.MapTest.OverMap.imagen, self.MapTest.mapa.rect)
            if self.MobBar_act:
                self.MapTest.MobsHpBarsUpdate(self.screen)
            self.I.FastSurfacesUpdate(hubo_colision)
            if self.I.jugador.StartSpell:
                self.I.jugador.Spell.update(self.screen, self.I.jugador, hubo_colision)
            self.I.update(self.bag_act, self.runes_act, self.char_act, self.equip_act, self.cursor)
            self.ItemDescription()
            
            pygame.display.update() #.flip()
        pygame.quit()

    def bucle_partida(self):
        pygame.mixer.music.load('music/opening.mid')
        pygame.mixer.music.play(loops=-1)
        
        timer = 0 
        
        background_image = load_image('graphics/background.jpg')
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        bg_rect = background_image.get_rect()
        
        logo_1 = Image('graphics/logo_1.png', left=100, top=10)
        logo_2 = Image('graphics/logo_2.png', left=100, top=10)
        logo_3 = Image('graphics/logo_3.png', left=100, top=10)
        logo_4 = Image('graphics/logo_4.png', left=100, top=10)
        
        (b1, b2, b3) = ('graphics/ground_b1.png', 'graphics/ground_b2.png', 'graphics/ground_b3.png')
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """Primer menu"""
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
         
        start_b = Button(b1, b2, b3, text="Entrar", size=12, color=(255,255,255), x=9, y=240, OnClick="Start")
        regis_b = Button(b1, b2, b3, text="Registrar", size=12, color=(255,255,255), x=144, y=240, OnClick="Register")
        exit_b = Button(b1, b2, b3, text="Salir", size=12, color=(255,255,255), x=278, y=240, OnClick="Exit")
        
        start_img1 = Image('graphics/ground_1.png')
        start_img2 = Image('graphics/ground_2.png', left=6, top=7)
                
        partida_window = Window(width=392, height=292, left=0, top=0, moveable=True)
        (partida_window.rect.centerx, partida_window.rect.centery) = (WIDTH/2, HEIGHT/2)
        partida_window.appendButton(start_b)
        partida_window.appendButton(regis_b)
        partida_window.appendButton(exit_b)
        partida_window.appendBGImage(start_img1)
        partida_window.appendBGImage(start_img2)
        
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """Segundo menu"""
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        enter_b = Button(b1, b2, b3, text="Aceptar", size=12, color=(255,255,255), x=15, y=77, OnClick="Accept")
        cancel_b = Button(b1, b2, b3, text="Cancelar", size=12, color=(255,255,255), x=143, y=77, OnClick="Cancel")
        
        login_img = Image('graphics/ground_1.png')
        login_img_surface = Contructor('graphics/c_0.png', 'graphics/c_1.png', 265, 130, (65,65,65))
        login_img.ChangeImage(login_img_surface)
        UsernameText = Text(text="User:", size=17, color=(235,235,235), left=30, top=24, font="Bell MT")
        PasswordText = Text(text="Password:", size=17, color=(235,235,235), left=30, top=53, font="Bell MT")
        TextEntryText = TextEntry(left=98, top=18, width=130, height=20)
        PassEntryText = TextEntry(password=True, left=98, top=47, width=130, height=20)
        
        login_window = Window(width=265, height=130, left=0, top=0, moveable=True)
        (login_window.rect.centerx, login_window.rect.centery) = (WIDTH/2, HEIGHT/2+95)
        login_window.appendBGImage(login_img)
        login_window.appendButton(enter_b)
        login_window.appendButton(cancel_b)
        login_window.appendTextEntry(TextEntryText)
        login_window.appendTextEntry(PassEntryText)
        login_window.appendText(UsernameText)
        login_window.appendText(PasswordText)
        
        Login = False
        
        while True:
            self.clock.tick(60)
            timer +=1
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if Login:
                    login_window.EntryEvents(event, keys)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    print event.key
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not Login:
                            if partida_window.collide(self.cursor):
                                pygame.mixer.Sound('sound/Cursor1.wav').play()
                        else:
                            if login_window.collide(self.cursor):
                                pygame.mixer.Sound('sound/Cursor1.wav').play()
                    elif event.button == 3:
                        pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not Login:
                        click_partida = partida_window.collide(1)
                        if click_partida == "Start":
                            Login = True
                        elif click_partida == "Register":
                            print click_partida
                        elif click_partida == "Exit":
                            pygame.quit()
                            sys.exit()
                    else:
                        click_login = login_window.collide(1)
                        if click_login == "Accept":
                            return None
                        elif click_login == "Cancel":
                            Login = False
            self.screen.fill((0,100,20))
            self.cursor.update()
            self.screen.blit(background_image, bg_rect)
            if timer<=5:
                logo_1.update(self.screen)
            elif timer<=10:
                logo_2.update(self.screen)
            elif timer<=15:
                logo_3.update(self.screen)
            else:
                logo_4.update(self.screen)
                if timer==800:
                    timer = 0
            if not Login:
                partida_window.update(self.screen, self.cursor)
            else:
                login_window.update(self.screen, self.cursor)
            pygame.display.update()
            
    def ItemDescription(self):
        for i in range(len(self.I.BagWindow.receptors)):
            if self.I.BagWindow.receptors[i].state:
                if self.I.BagWindow.objects[i].rect.colliderect(self.cursor):
                    if not self.I.ShowII_act_b:
                        self.I.ItemInfo(self.cursor, ("i", i))
                        return False
                    else:
                        return False
        self.I.ShowII_act_b = False
        for c in range(len(self.I.EquipWindow.receptors)):
            if self.I.EquipWindow.receptors[c].state:
                if self.I.EquipWindow.objects[c].rect.colliderect(self.cursor):
                    if not self.I.ShowII_act_e:
                        self.I.ItemInfo(self.cursor, ("c", c))
                        #self.I.ShowII_act = True
                        return False
                    else:
                        return False
        self.I.ShowII_act_e = False
    def Hotkeys(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if not self.I.jugador.SpellReady:
                        atk = self.I.jugador.atacar(self.MapTest.mobs)
                        if atk != 0 and self.delayAtk>60:
                            self.Atk(atk-1)
                    else:
                        self.ActivateSpell()
                elif event.key == pygame.K_b:
                    self.OpenBag()
                elif event.key == pygame.K_ESCAPE:
                    self.Pause()
                elif event.key == pygame.K_s:
                    self.SkillStones()
                elif event.key == pygame.K_r:
                    self.Runes()
                elif event.key == pygame.K_c:
                    self.Character()
                elif event.key == pygame.K_e:
                    self.Equip()
                elif event.key == pygame.K_v:
                    self.MobsHPBars()
                elif event.key == pygame.K_SPACE:
                    self.Talk()
                    f = self.RecogerItem()
                    if f:
                        self.RecogerItem(1, f-1)
                elif event.key == pygame.K_m:
                    self.OpenMap()
                elif event.key == pygame.K_F1:
                    self.UseSkill(1)
                elif event.key == pygame.K_F2:
                    self.UseSkill(2)
                elif event.key == pygame.K_F3:
                    self.UseSkill(3)
                elif event.key == pygame.K_F4:
                    self.UseSkill(4)
                elif event.key == pygame.K_F5:
                    self.UseSkill(5)
                elif event.key == pygame.K_F6:
                    self.UseSkill(6)
                elif event.key == pygame.K_F7:
                    self.UseSkill(7)
                elif event.key == pygame.K_F8:
                    self.UseSkill(8)
                elif event.key == pygame.K_F9:
                    self.UseSkill(9)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.I.menu_buttons_window.collide(self.cursor):
                        pygame.mixer.Sound('sound/Cursor1.wav').play()
                    self.I.rune_window.collide(self.cursor)
                    self.I.skillbar_window.collide(self.cursor)
                    self.I.CharWindow.collide(self.cursor)
                    self.I.BagWindow.collide(self.cursor)
                    self.I.EquipWindow.collide(self.cursor)
                elif event.button == 3:
                    if self.bag_act:
                        self.UseItem()
            elif event.type == pygame.MOUSEBUTTONUP:
                click_menu = self.I.menu_buttons_window.collide(1)
                self.I.skillbar_window.collide(1)
                self.I.rune_window.collide(1)
                self.I.CharWindow.collide(1)
                self.I.BagWindow.collide(1)
                self.I.EquipWindow.collide(1)
                
                if click_menu == "Bag":
                    self.OpenBag()
                elif click_menu == "Char":
                    self.Character()
                elif click_menu == "Equip":
                    self.Equip()
                    
    def Atk(self,i):
        pygame.mixer.Sound('sound/Damage.wav').play()
        self.delayAtk = 0
        self.DamageFastSurface(i)
        if self.MapTest.mobs[i].hp <= 0:
            self.MobKill(i)
        else:
            self.MapTest.mobs[i].hprect = pygame.Rect((0, 0), (self.MapTest.mobs[i].hp*28.0/self.MapTest.mobs[i].maxhp, 3))
    def Pause(self):
        pass
    def SkillStones(self):
        pass
    def Character(self):
        if self.char_act:
            self.char_act = False
        else:
            self.char_act = True
    def Equip(self):
        if self.equip_act:
            self.equip_act = False
        else:
            self.equip_act = True
    def Runes(self):
        if self.runes_act:
            self.runes_act = False
        else:
            self.runes_act = True
    def OpenBag(self):
        if self.bag_act:
            self.bag_act = False
        else:
            self.bag_act = True
    def Talk(self):
        pass
    def OpenMap(self):
        pass
    def MobsHPBars(self):
        if self.MobBar_act:
            self.MobBar_act = False
        else:
            self.MobBar_act = True
    def ActivateSpell(self):
        self.I.jugador.StartSpell = True
        mob_ind = self.I.jugador.atacar(self.MapTest.mobs, spell=True)
        if mob_ind:
            mob_ind -= 1 
            self.DamageFastSurface(mob_ind, self.I.jugador.Spell.Damage)
            if self.MapTest.mobs[mob_ind].hp <= 0:
                self.MobKill(mob_ind)
            else:
                self.MapTest.mobs[mob_ind].hprect = pygame.Rect((0, 0), (self.MapTest.mobs[mob_ind].hp*28.0/self.MapTest.mobs[mob_ind].maxhp, 3))
        self.I.jugador.UsingSpell = False
        pygame.mixer.Sound('sound/spellsound.wav').play()
    def UseSkill(self,n):
        pygame.mixer.Sound('sound/BeginSpell.wav').play()
        if n == 1:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Fire_sc', self.I.jugador, 10)
            self.I.jugador.UseSpell()
        elif n == 2:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Fire_sl', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 3:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Fire_ex', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 4:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Ignus_rg', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 5:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Ignus_st', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 6:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Fire_bl', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 7:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Fire_dc', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 8:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Ignus_bl', self.I.jugador, 1)
            self.I.jugador.UseSpell()
        elif n == 9:
            self.I.jugador.DeleteSpell()
            self.I.jugador.Spell = Spell('Ignus_ex', self.I.jugador, 1)
            self.I.jugador.UseSpell()
    def MobKill(self,i):
        self.I.jugador.exp += self.MapTest.mobs[i].exp
        self.I.jugador.soul_points += self.MapTest.mobs[i].nivel
        
        if self.I.jugador.exp >= self.I.jugador.exp_nivel:
            self.I.jugador.SubirNivel()
            self.I.CharWindowUpdate([0,8,9,10,13,14])
        self.I.CharWindowUpdate([1,15])
        self.I.barra_estado_info()
        drop = self.MapTest.mobs[i].drops
        rect = self.MapTest.mobs[i].rect
        self.I.FastSurfaces.append(FastSurface(text="+"+str(self.MapTest.mobs[i].nivel)+" Souls", size=11, color=(10,10,200), left=self.I.jugador.rect.left+7, top=self.I.jugador.rect.top-20, retard=40))
        self.I.FastSurfaces.append(FastSurface(text="+"+str(self.MapTest.mobs[i].exp)+" EXP", size=11, color=(10,10,200), left=self.I.jugador.rect.left+7, top=self.I.jugador.rect.top-20, retard=20))
        self.MapTest.mobs = self.MapTest.mobs[:i] + self.MapTest.mobs[i+1:]
        r = random.randint(1,1000)
        self.Dropear(drop, r, rect)
    def Dropear(self, drop, r, rect):
        if r <=300:
            if 300 > r > 100:
                IDs = iDropToID('HP_POTION')
            elif r > 50:
                IDs = iDropToID(drop)
            elif r > 10:
                IDs = iDropToID(drop) #Equipo mejorado
            else:
                IDs = iDropToID(drop) #Runas y Skill's Stones
            self.DroppedItems.append(Item(random.choice(IDs), rect))
            
        else:
            IDs = iDropToID(drop) #Runas y Skill's Stones
            self.DroppedItems.append(Item(random.choice(IDs), rect))
    def ItemDropUpdate(self, hubo_colision):
        for i in self.DroppedItems:
            image = load_image("graphics/item/chest.png", True)
            i.update(self.screen, image, self.I.jugador, hubo_colision)
    def RecogerItem(self, r = False, i = None, item = None):
        if r:
            x = 0
            for c in range(len(self.I.BagWindow.receptors)):
                if self.I.BagWindow.receptors[c].state==False:
                    for cont in range(len(self.I.jugador.bag)):
                        if self.I.jugador.bag[cont] == None:
                            if item == None:
                                self.I.jugador.bag[cont] = self.DroppedItems[i]
                                self.I.ObjectsBag(c, cont)
                            else:
                                self.I.jugador.bag[cont] = item
                                self.I.ObjectsBag(c, cont)
                                return 0
                            x = 1
                            break
                if x == 1:
                    break
            if not x:
                if item == None:
                    self.I.jugador.bag.append(self.DroppedItems[i])
                    self.I.AppendObjectsBag()
                else:
                    self.I.jugador.bag.append(item)
                    self.I.AppendObjectsBag()
                    return 0
            self.DroppedItems = self.DroppedItems[:i] + self.DroppedItems[i+1:]
        else:
            for i in range(len(self.DroppedItems)):
                if self.I.jugador.rect.colliderect(self.DroppedItems[i].rect_inv):
                    return i+1
            return 0
    def UseItem(self):
        for c in range(len(self.I.jugador.bag)):
            obj = self.I.BagWindow.objects[c]
            if obj.rect.colliderect(self.cursor):
                if self.I.jugador.bag[obj.reference].tipo != 'P':
                    self.EquiparItem(self.I.jugador.bag[obj.reference], c)
                    return 0
                else:
                    self.UsarPocion(self.I.jugador.bag[obj.reference].fx, c)
                    return 0
    def EquiparItem(self, item, c):
        tipo = item.tipo
        if tipo == "W": x = 0
        elif tipo == "A": x = 1
        elif tipo == "HG": x = 2
        elif tipo == "FG": x = 3
        
        if self.I.jugador.equip[x] == None:
            self.I.jugador.equip[x] = item
        else:
            ii = self.I.jugador.equip[x]
            self.RecogerItem(1, None, ii)
            self.I.jugador.equip[x] = item
            self.EquipBonus(0, ii)
        self.I.ObjectsEquip(x)
        self.EquipBonus(1, item)
        self.I.barra_estado_info()
        self.I.jugador.bag[self.I.BagWindow.objects[c].reference] = None
        self.I.BagWindow.objects[c] = Object()
        self.I.BagWindow.receptors[c].state = False
    def EquipBonus(self, v, item):
        L = []
        if v == 1:
            self.I.jugador.str += 0
            self.I.jugador.int += 0
            self.I.jugador.agi += 0
            self.I.jugador.dex += 0
            self.I.jugador.vit += 0
            self.I.jugador.atack += int(item.atack)
            self.I.jugador.defense += int(item.defense)
            self.I.jugador.dodge += 0
            self.I.jugador.crit += 0
            self.I.jugador.maxhp += int(item.maxhp)
            self.I.jugador.maxsp += int(item.maxsp)
            
            if (int(item.atack)):
                L.append(9)
            if (int(item.defense)):
                L.append(10)
            if (int(item.maxhp)):
                L.append(13)
            if (int(item.maxsp)):
                L.append(14)
            self.I.CharWindowUpdate(L)
        else:
            self.I.jugador.str -= 0
            self.I.jugador.agi -= 0
            self.I.jugador.dex -= 0
            self.I.jugador.vit -= 0
            self.I.jugador.atack -= int(item.atack)
            self.I.jugador.defense -= int(item.defense)
            self.I.jugador.dodge -= 0
            self.I.jugador.crit -= 0
            self.I.jugador.maxhp -= int(item.maxhp)
            self.I.jugador.maxsp -= int(item.maxsp)
            
            if (int(item.atack)):
                L.append(9)
            if (int(item.defense)):
                L.append(10)
            if (int(item.maxhp)):
                L.append(13)
            if (int(item.maxsp)):
                L.append(14)
            self.I.CharWindowUpdate(L)
            
    def DamageFastSurface(self, i, spell_damage=None):
        if spell_damage == None:
            damage = (self.I.jugador.dano() - self.MapTest.mobs[i].defense)
        else:
            damage = self.DamageSpellCalculator(spell_damage)
        if damage>0:
            self.I.FastSurfaces.append(FastSurface(text="-"+str(damage), color=(225,0,0), left=self.MapTest.mobs[i].rect.left+7, top=self.MapTest.mobs[i].rect.top-20))
        else:
            self.I.FastSurfaces.append(FastSurface(text="Resistido", color=(225,0,0), left=self.MapTest.mobs[i].rect.left+7, top=self.MapTest.mobs[i].rect.top-20))
        self.MapTest.mobs[i].hp-= damage
    def DamageSpellCalculator(self, damage):
        return int(damage)
    def UsarPocion(self, fx, c):
        self.I.jugador.bag[self.I.BagWindow.objects[c].reference] = None
        self.I.BagWindow.objects[c] = Object()
        self.I.BagWindow.receptors[c].state = False

Game = RPG()
