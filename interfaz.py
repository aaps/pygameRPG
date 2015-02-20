import pygame, sys
from sprite import *
from gui import *
from engine import WIDTH, HEIGHT, velocidad

class InterfazJuego:
    def __init__(self,screen):
        self.fuente = pygame.font.Font("TrajanPro-Bold.otf", 16)
        self.jugador = Personaje(velocidad,WIDTH,HEIGHT)
        self.screen = screen
        self.FastSurfaces = []
        
        #Barra Estado Info        
        HP = Text(text=(str(self.jugador.hp)+"/"+str(self.jugador.maxhp)), size=13, color=(255,255,255), left=190, top=5)
        SP = Text(text=(str(self.jugador.sp)+"/"+str(self.jugador.maxsp)), size=13, color=(255,255,255), left=190, top=35)
        EXP = Text(text=(str(self.jugador.exp)+"/"+str(self.jugador.exp_nivel)), size=13, color=(255,255,255), left=190, top=65)
        
        bar_image1 = Image('graphics/main_bar.png', left=0, top=0)
        bar_image2 = Image('graphics/main_bar.png', left=0, top=30)
        bar_image3 = Image('graphics/main_bar.png', left=0, top=60)
        
        self.main_bars = Window(width=250, height=27, left=10, top=10)
        
        self.main_bars.appendText(HP)
        self.main_bars.appendText(SP)
        self.main_bars.appendText(EXP)
        
        self.main_bars.appendImage(bar_image1)
        self.main_bars.appendImage(bar_image2)
        self.main_bars.appendImage(bar_image3)
        
        self.hp_rect = pygame.Rect(10, 10, 240, 20)
        self.sp_rect = pygame.Rect(10, 40, 240, 20)
        self.exp_rect = pygame.Rect(10, 70, 0, 20)
        
        #Bag Window
        bag_image = Image('graphics/inventory.png')
        (a, b) = ('graphics/inventory_light1.png', 'graphics/inventory_light.png')

        self.BagWindow = Window(width=bag_image.rect.w, height=bag_image.rect.h, left=WIDTH-170, top=HEIGHT-300, moveable=True)
        self.BagWindow.appendBGImage(bag_image)
        
        for y in range(6):
            for x in range(5):
                self.BagWindow.appendButton(Button(a, b, b, x=10+x*27, y=32+y*27))
                self.BagWindow.appendObject(Object())
                self.BagWindow.appendReceptor(Receptor(Type="Inventory", left=10+x*27, top=32+y*27, width=24, height=24))
                
        #Char Window
        char_image = Image('graphics/character.png', left=0, top=0)
        char_w_lv = Text(text="Lv: "+str(self.jugador.nivel), size=12, color=(209,195,137), left=20, top=53)
        char_w_exp = Text(text="Exp: "+str(round(self.jugador.exp*100.0/self.jugador.exp_nivel,2))+"%", size=12, color=(209,195,137), left=100, top=53)
        char_w_prof = Text(text="Job: "+self.jugador.especializacion, size=12, color=(209,195,137), left=20, top=53+15)
        char_w_str = Text(text="Str: "+str(self.jugador.str+self.jugador.str_b), size=12, color=(209,195,137), left=20, top=74+15)
        char_w_dex = Text(text="Dex: "+str(self.jugador.dex+self.jugador.dex_b), size=12, color=(209,195,137), left=100, top=74+15)
        char_w_int = Text(text="Int: "+str(self.jugador.int+self.jugador.int_b), size=12, color=(209,195,137), left=20, top=74+15*2)
        char_w_vit = Text(text="Vit: "+str(self.jugador.vit+self.jugador.vit_b), size=12, color=(209,195,137), left=100, top=74+15*2)
        char_w_agi = Text(text="Agi: "+str(self.jugador.agi+self.jugador.agi_b), size=12, color=(209,195,137), left=20, top=74+15*3)
        char_w_stats = Text(text="Points: "+str(self.jugador.stat_points), size=12, color=(209,195,137), left=60, top=74+15*4)
        char_w_atk = Text(text="Atk: "+str(self.jugador.atack+self.jugador.atack_b), size=12, color=(209,195,137), left=20, top=156)
        char_w_def = Text(text="Def: "+str(self.jugador.defense+self.jugador.defense_b), size=12, color=(209,195,137), left=100, top=156)
        char_w_lth = Text(text="Lth: "+str(float(self.jugador.crit+self.jugador.crit_b))+"%", size=12, color=(209,195,137), left=20, top=156+15)
        char_w_dge = Text(text="Dge: "+str(float(self.jugador.dodge+self.jugador.dodge_b))+"%", size=12, color=(209,195,137), left=100, top=156+15)
        char_w_mhp = Text(text="MHP: "+str(self.jugador.maxhp+self.jugador.maxhp_b), size=12, color=(209,195,137), left=20, top=156+15*2)
        char_w_msp = Text(text="MSP: "+str(self.jugador.maxsp+self.jugador.maxsp_b), size=12, color=(209,195,137), left=100, top=156+15*2)
        char_w_SoulE = Text(text="Soul's Essences: "+str(self.jugador.soul_points), size=12, color=(209,195,137), left=20, top=209)
        char_w_StoneE = Text(text="Stone's Essences: "+str(self.jugador.stone_points), size=12, color=(209,195,137), left=20, top=209+15)
        char_w_ctrl = Text(text="Control: ", size=12, color=(209,195,137), left=20, top=209+15*2)
        char_w_gold = Text(text="Gold: "+str(self.jugador.cash), size=12, color=(209,195,137), left=20, top=260)
        
        self.CharWindow = Window(width=char_image.rect.w, height=char_image.rect.h, moveable=True)
        self.CharWindow.rect.center = (WIDTH/2, HEIGHT/2)
        
        self.CharWindow.appendBGImage(char_image)
        self.CharWindow.appendText(char_w_lv)
        self.CharWindow.appendText(char_w_exp)
        self.CharWindow.appendText(char_w_prof)
        self.CharWindow.appendText(char_w_str)
        self.CharWindow.appendText(char_w_dex)
        self.CharWindow.appendText(char_w_int)
        self.CharWindow.appendText(char_w_vit)
        self.CharWindow.appendText(char_w_agi)
        self.CharWindow.appendText(char_w_stats)
        self.CharWindow.appendText(char_w_atk)
        self.CharWindow.appendText(char_w_def)
        self.CharWindow.appendText(char_w_lth)
        self.CharWindow.appendText(char_w_dge)
        self.CharWindow.appendText(char_w_mhp)
        self.CharWindow.appendText(char_w_msp)
        self.CharWindow.appendText(char_w_SoulE)
        self.CharWindow.appendText(char_w_StoneE)
        self.CharWindow.appendText(char_w_ctrl)
        self.CharWindow.appendText(char_w_gold)

        #Equipement Window
        equip_image = Image('graphics/equipement.png', left=0, top=0)
        
        self.EquipWindow = Window(width=equip_image.rect.w, height=equip_image.rect.h, moveable=True)
        (self.EquipWindow.rect.left, self.EquipWindow.rect.top) =(WIDTH-300, HEIGHT-400)
        
        self.EquipWindow.appendBGImage(equip_image)
        
        for y in range(2):
            for x in range(4):
                self.EquipWindow.appendObject(Object())
                self.EquipWindow.appendReceptor(Receptor(Type="Equip", width=24, height=24, left=x*41+23, top=y*48+28))
        
        self.ShowII_act_e = False
        self.ShowII_act_b = False
        
        #Rune windows
        rune_image = Image('graphics/runes.png')
        self.rune_window = Window(rune_image.rect.w, rune_image.rect.h, WIDTH/2, HEIGHT/2, moveable=True)
        self.rune_window.appendImage(rune_image)
    
        #Botones del menu
        (mbu1, mbu2, mbu3) = ("graphics/menu_button_1.png", "graphics/menu_button_2.png", "graphics/menu_button_3.png") 
        mb1 = Button(mbu1, mbu2, mbu3, text="Bag", size=14, color=(255,255,255), x=0, y=0, OnClick="Bag")
        mb2 = Button(mbu1, mbu2, mbu3, text="Skill", size=14, color=(255,255,255), x=89, y=0)
        mb3 = Button(mbu1, mbu2, mbu3, text="Char", size=14, color=(255,255,255), x=178, y=0, OnClick="Char")
        mb4 = Button(mbu1, mbu2, mbu3, text="Equip", size=14, color=(255,255,255), x=0, y=39, OnClick="Equip")
        mb5 = Button(mbu1, mbu2, mbu3, text="Map", size=14, color=(255,255,255), x=89, y=39)
        mb6 = Button(mbu1, mbu2, mbu3, text="Options", size=14, color=(255,255,255), x=178, y=39)
        
        self.menu_buttons_window = Window(width=270, height=80, left=WIDTH-275, top=HEIGHT-87, moveable=True)
        self.menu_buttons_window.appendButton(mb1)
        self.menu_buttons_window.appendButton(mb2)
        self.menu_buttons_window.appendButton(mb3)
        self.menu_buttons_window.appendButton(mb4)
        self.menu_buttons_window.appendButton(mb5)
        self.menu_buttons_window.appendButton(mb6)
        
        #Butones de skill
        sk_bar_image = Image('graphics/skill_bar.png')
        b1 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22, y=5)
        b2 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+45, y=5)
        b3 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+2*45, y=5)
        b4 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+3*45, y=5)
        b5 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+4*45, y=5)
        b6 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+5*45, y=5)
        b7 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+6*45, y=5)
        b8 = Button("graphics/skill_b1.png", "graphics/skill_b2.png", "graphics/skill_b1.png", x=22+7*45, y=5)
        self.skillbar_window = Window(width=395, height=48, left=10, top=HEIGHT-60, moveable=True)
        self.skillbar_window.appendBGImage(sk_bar_image)
        self.skillbar_window.appendButton(b1)
        self.skillbar_window.appendButton(b2)
        self.skillbar_window.appendButton(b3)
        self.skillbar_window.appendButton(b4)
        self.skillbar_window.appendButton(b5)
        self.skillbar_window.appendButton(b6)
        self.skillbar_window.appendButton(b7)
        self.skillbar_window.appendButton(b8)
            
        
    def barra_estado_info(self):
        (x0, y0) = (self.main_bars.rect.left, self.main_bars.rect.top)
        HP = Text(text=(str(self.jugador.hp)+"/"+str(self.jugador.maxhp)), size=13, color=(255,255,255), left=0, top=5+y0)
        SP = Text(text=(str(self.jugador.sp)+"/"+str(self.jugador.maxsp)), size=13, color=(255,255,255), left=0, top=35+y0)
        EXP = Text(text=(str(self.jugador.exp)+"/"+str(self.jugador.exp_nivel)), size=13, color=(255,255,255), left=0, top=65+y0)
        HP.rect.right = self.main_bars.rect.right-15
        SP.rect.right = self.main_bars.rect.right-15
        EXP.rect.right = self.main_bars.rect.right-15
        self.main_bars.texts[0] = HP
        self.main_bars.texts[1] = SP
        self.main_bars.texts[2] = EXP
        self.exp_rect = pygame.Rect(10, 70, self.jugador.exp*240/self.jugador.exp_nivel, 20)
        self.hp_rect = pygame.Rect(10, 10, self.jugador.hp*240/self.jugador.maxhp, 20)
        
        
    def pintar_barras(self):
        pygame.draw.rect(self.screen, (236,61,43), self.hp_rect)
        pygame.draw.rect(self.screen, (94,135,239), self.sp_rect)
        pygame.draw.rect(self.screen, (94,239,60), self.exp_rect)
        
        
    def update(self, Bag, Runes, Char, Equip, cursor):
        self.pintar_barras()
        self.skillbar_window.update(self.screen, cursor)
        self.main_bars.update(self.screen, cursor)
        self.menu_buttons_window.update(self.screen, cursor)
        if Runes:
            self.rune_window.update(self.screen, cursor)
        if Char:
            self.CharWindow.update(self.screen, cursor)
        if Equip:
            self.EquipWindow.update(self.screen, cursor)
        if Bag:
            self.BagWindow.update(self.screen, cursor)
            if self.ShowII_act_b:
                self.ItemInfoWindow.update(self.screen, cursor)
        if Equip:
            if self.ShowII_act_e:
                self.ItemInfoWindow.update(self.screen, cursor)

    def ItemsBag(self):
        (l, t) = (self.BagWindow.rect.left+10, self.BagWindow.rect.top+32)
        (x, y) = (0 ,0)
        for i in range(len(self.jugador.bag)):
            try:
                self.jugador.bag[i].rect_inv = pygame.Rect(l+x*27,t+y*27,24,24)
            except: pass
            x += 1
            if x == 5:
                x = 0
                y += 1
    def ObjectsEquip(self, ind):
        (l, t) = (self.EquipWindow.rect.left+23, self.EquipWindow.rect.top+28)
        (x, y) = ( l+(ind-(ind/4)*4)*41, t+(ind/4)*48 )
        self.EquipWindow.objects[ind] = Object(image=self.jugador.equip[ind].image_inv, left=x, top=y, width=24, height=24, moveable=False, reference=ind)
        self.EquipWindow.receptors[ind].state = True
    def ObjectsBag(self, ind, ind_i):
        (l, t) = (self.BagWindow.rect.left+10, self.BagWindow.rect.top+32)
        (x, y) = ( l+(ind-(ind/5)*5)*27, t+(ind/5)*27 )
        self.BagWindow.objects[ind] = Object(image=self.jugador.bag[ind_i].image_inv, left=x, top=y, width=24, height=24, moveable=True, reference=ind_i)
        self.BagWindow.receptors[ind].state = True 
    def ItemInfo(self, cursor, (tipe, ind)):                  
        if tipe == "i":
            item = self.jugador.bag[self.BagWindow.objects[ind].reference]
            self.ItemInfoWindow = Window(width=0, height=0, left=self.BagWindow.rect.left-200, top=self.BagWindow.rect.top+1, moveable=1)
            self.ShowII_act_b = True
        elif tipe == "c":
            item = self.jugador.equip[self.EquipWindow.objects[ind].reference]
            self.ItemInfoWindow = Window(width=0, height=0, left=self.EquipWindow.rect.right, top=self.EquipWindow.rect.top+1, moveable=1)
            self.ShowII_act_e = True
        else:
            item = 0
            self.ShowII_act_e = False
            self.ShowII_act_b = False
        if item != 0:
            
            bg_image = Image('graphics/iteminfo_bg.png')
            des_image = Image(item.image_des, left=13, top=34)
            nombre = Text(text=item.nombre, size=12, color=(255,255,255), left=5, top=7)

            if item.tipo == "W":
                tipo = Text(text="Tipo: Arma", size=11, left=93, top=34)
            elif item.tipo == "A":
                tipo = Text(text="Tipo: Armadura", size=11, left=93, top=34)
            elif item.tipo == "FG":
                tipo = Text(text="Tipo: Zapatos", size=11, left=93, top=34)
            elif item.tipo == "HG":
                tipo = Text(text="Tipo: Sombrero", size=11, left=93, top=34)
            elif item.tipo == "P":
                tipo = Text(text="Tipo: Pocion", size=11, left=93, top=34)
                
            c = 0
            if item.atack:
                c+=1
                atk = Text(text="Atk: "+str(item.atack), size=11, left=94, top=34+c*12)
                self.ItemInfoWindow.appendText(atk)
            if item.defense:
                c+=1
                defe = Text(text="Def: "+str(item.defense), size=11, left=94, top=34+c*12)
                self.ItemInfoWindow.appendText(defe)
            if item.maxhp:
                c+=1
                hp =Text(text="MaxHP+ "+str(item.maxhp), size=11, left=94, top=34+c*12)
                self.ItemInfoWindow.appendText(hp)
            if item.maxsp:
                c+=1
                sp =Text(text="MaxSP+ "+str(item.maxsp), size=11, left=94, top=34+c*12)
                self.ItemInfoWindow.appendText(sp) 
        
            self.ItemInfoWindow.appendBGImage(bg_image)
            self.ItemInfoWindow.appendImage(des_image)
            self.ItemInfoWindow.appendText(nombre)
            self.ItemInfoWindow.appendText(tipo)
            
            
    def FastSurfacesUpdate(self, hubo_colision):
        for s in self.FastSurfaces:
            s.update(self.screen, self.jugador, hubo_colision)
            for i in range(len(self.FastSurfaces)):
                if self.FastSurfaces[i].Delete:
                    self.FastSurfaces = self.FastSurfaces[:i] + self.FastSurfaces[i+1:]
                    break
                
    def CharWindowUpdate(self, stats):
        (x,y) = (self.CharWindow.rect.left, self.CharWindow.rect.top)       
        for ind in stats:
            if ind == 0:
                self.CharWindow.texts[ind] = Text(text="Lv: "+str(self.jugador.nivel), size=12, color=(209,195,137), left=20+x, top=53+y)
            elif ind == 1:
                self.CharWindow.texts[ind] = Text(text="Exp: "+str(round(self.jugador.exp*100.0/self.jugador.exp_nivel,2))+"%", size=12, color=(209,195,137), left=100+x, top=53+y)
            elif ind == 2:
                self.CharWindow.texts[ind] = Text(text="Job: "+self.jugador.especializacion, size=12, color=(209,195,137), left=20+x, top=53+15+y)
            elif ind == 3:
                self.CharWindow.texts[ind] = Text(text="Str: "+str(self.jugador.str+self.jugador.str_b), size=12, color=(209,195,137), left=20+x, top=74+15+y)
            elif ind == 4:
                self.CharWindow.texts[ind] = Text(text="Dex: "+str(self.jugador.dex+self.jugador.dex_b), size=12, color=(209,195,137), left=100+x, top=74+15+y)
            elif ind == 5:
                self.CharWindow.texts[ind] = Text(text="Int: "+str(self.jugador.int+self.jugador.int_b), size=12, color=(209,195,137), left=20+x, top=74+15*2+y)
            elif ind == 6:
                self.CharWindow.texts[ind] = Text(text="Vit: "+str(self.jugador.vit+self.jugador.vit_b), size=12, color=(209,195,137), left=100+x, top=74+15*2+y)
            elif ind == 7:
                self.CharWindow.texts[ind] = Text(text="Agi: "+str(self.jugador.agi+self.jugador.agi_b), size=12, color=(209,195,137), left=20+x, top=74+15*3+y)
            elif ind == 8:
                self.CharWindow.texts[ind] = Text(text="Points: "+str(self.jugador.stat_points), size=12, color=(209,195,137), left=60+x, top=74+15*4+y)
            elif ind == 9:
                self.CharWindow.texts[ind] = Text(text="Atk: "+str(self.jugador.atack+self.jugador.atack_b), size=12, color=(209,195,137), left=20+x, top=156+y)
            elif ind == 10:
                self.CharWindow.texts[ind] = Text(text="Def: "+str(self.jugador.defense+self.jugador.defense_b), size=12, color=(209,195,137), left=100+x, top=156+y)
            elif ind == 11:
                self.CharWindow.texts[ind] = Text(text="Lth: "+str(float(self.jugador.crit+self.jugador.crit_b))+"%", size=12, color=(209,195,137), left=20+x, top=156+15+y)
            elif ind == 12:
                self.CharWindow.texts[ind] = Text(text="Dge: "+str(float(self.jugador.dodge+self.jugador.dodge_b))+"%", size=12, color=(209,195,137), left=100+x, top=156+15+y)
            elif ind == 13:
                self.CharWindow.texts[ind] = Text(text="MHP: "+str(self.jugador.maxhp+self.jugador.maxhp_b), size=12, color=(209,195,137), left=20+x, top=156+15*2+y)
            elif ind == 14:
                self.CharWindow.texts[ind] = Text(text="MSP: "+str(self.jugador.maxsp+self.jugador.maxsp_b), size=12, color=(209,195,137), left=100+x, top=156+15*2+y)
            elif ind == 15:
                self.CharWindow.texts[ind] = Text(text="Soul's Essences: "+str(self.jugador.soul_points), size=12, color=(209,195,137), left=20+x, top=209+y)
            elif ind == 16:
                self.CharWindow.texts[ind] = Text(text="Stone's Essences: "+str(self.jugador.stone_points), size=12, color=(209,195,137), left=20+x, top=209+15+y)
            elif ind == 17:
                self.CharWindow.texts[ind] = Text(text="Control: ", size=12, color=(209,195,137), left=20+x, top=209+15*2+y)
            elif ind == 18:
                self.CharWindow.texts[ind] = Text(text="Gold: "+str(self.jugador.cash), size=12, color=(209,195,137), left=20+x, top=260+y)
 
 
class FastSurface:
    def __init__(self, text="Info", color=(0,0,0), size=15, retard=0, left=0, top=0):
        self.Retard = retard
        self.Surface = Text(text=str(text), size=size, color=color, left=left, top=top)
        self.Time = 0
        self.Count = 0
        self.Delete = False  
    def update(self, screen, pj, colision):
        if self.Count == 60:
            self.Delete = True
            return 0
        self.Time += 1
        if self.Time >= self.Retard:
            self.Count += 1 
            self.Surface.Move([0, -1])
            if not colision:
                self.Surface.Move([-pj.vx, -pj.vy])
            self.Surface.update(screen)
            
class Spell:
    def __init__(self, ID, Char, SpellLv):
        Spell = self.SearchSpell(ID)
        ruta = Spell[2]+'.png'
        Form = Spell[3].split(',')
        fil = Form[0]
        col = Form[1]
        frames = Form[2]
        
        self.SpellSprites = cortar_spell(ruta, fil, col, frames)
        self.Rect = self.SpellSprites[0].get_rect()
        self.Time = 0
        self.Delete = False
        
        self.MaxLvl = Spell[4]
        self.Damage = Spell[5].split(',')[SpellLv-1]
        self.Math = Spell[6]
        self.CastTime = float(Spell[8].split(',')[SpellLv-1])
        
    def update(self, screen, pj, colision):
        if self.Delete:
            return False
        if not colision:
            self.Rect.move_ip(-pj.vx, -pj.vy)
        self.ChangeSprite()
        screen.blit(self.Image, self.Rect)
        self.Time +=1
    
    def ChangeSprite(self):
        i = self.Time/3
        if i+1 > len(self.SpellSprites):
            self.Delete = True
            return False
        self.Image = self.SpellSprites[i]
    def SearchSpell(self, ID):
        DB = open('SpellDataBase.txt')
        for Spell in DB:
            SpellInfo = Spell.split('\t')
            if SpellInfo[0] == ID:
                return SpellInfo
                DB.close()
        DB.close()
        print "No se ha encontrado la Spell "+ID+" en nuestra base de datos."
        