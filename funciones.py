#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import base64
import gzip
import StringIO
import pygame
from pygame.locals import *


# Mapas
# ---------------------------------------------------------------------

def decodificar(cadena):
	# Decodificar.
	cadena = base64.decodestring(cadena)
	
	# Descomprimir.
	copmressed_stream = StringIO.StringIO(cadena)
	gzipper = gzip.GzipFile(fileobj=copmressed_stream)
	cadena = gzipper.read()
	
	# Convertir.
	salida = []
	for idx in xrange(0, len(cadena), 4):
		val = ord(str(cadena[idx])) | (ord(str(cadena[idx + 1])) << 8) | \
		(ord(str(cadena[idx + 2])) << 16) | (ord(str(cadena[idx + 3])) << 24)
		salida.append(val)
		
	return salida

# ---------------------------------------------------------------------

# Pygame
# ---------------------------------------------------------------------

# Carga una imagen transparencia y color tranasparente opcionales.
def load_image(filename, transparent=False, pixel=(0,0), alpha=False):
	try: image = pygame.image.load(filename)
	except pygame.error, message:
		raise SystemExit, message
	if not alpha:
		image = image.convert()
	else:
		image = image.convert_alpha()
	if transparent:
		color = image.get_at(pixel)
		image.set_colorkey(color, RLEACCEL)
	return image
# Corta un tilest y lo almacena en un array unidimensional.  
def cortar_tileset(ruta, (w, h)):
	image = load_image(ruta, True, alpha=1)
	rect = image.get_rect()
	col = rect.w / w
	fil = rect.h / h
	sprite = [None]
		
	for f in range(fil):
		for c in range(col):
			sprite.append(image.subsurface((rect.left, rect.top, w, h)))
			rect.left += w
		rect.top += h
		rect.left = 0
		
	return sprite


# Corta un chara en las fil y col indicadas. Array Bidimensional.
def cortar_chara(ruta, fil, col):
	image = load_image(ruta, True)
	rect = image.get_rect()
	w = rect.w / col
	h = rect.h / fil
	sprite = range(fil)
	for i in range(fil):
		sprite[i] = range(col)
	for f in range(fil):
		for c in range(col):
			sprite[f][c] = image.subsurface((rect.left, rect.top, w, h))
			rect.left += w
		rect.top += h
		rect.left = 0
	return sprite

def cortar_spell(ruta, col, fil, frames):
	image = load_image('graphics/Spells/'+ruta, alpha=True)
	rect = image.get_rect()
	w = rect.w / int(col)
	h = rect.h / int(fil)
	sprite = []
	for f in range(int(fil)):
		for c in range(int(col)):
			sprite.append(image.subsurface((rect.left, rect.top, w, h)))
			rect.left += w
		rect.top += h
		rect.left = 0
	return sprite[:int(frames)]

def colisionMap(player,rects):
	for rec in rects.colisiones:
		if player.rectcol.colliderect(rec):
			return True
	return False
def fuente(font=None, t=12):
	if font != None:
		return pygame.font.SysFont(font, t, False, False)
	else:
		return pygame.font.Font("TrajanPro-Bold.otf", t)

def iDropToID(drop):
	ItemClase = open("ItemClase.txt")
	for Clase in ItemClase:
		if drop in Clase:
			l = Clase[(Clase.find("{")+1):Clase.find("}")]
			return ItemsIDs(l)
def Contructor(img1, img2, width, height, color=(0,0,0)):
	Esquinas = []
	Laterales = []
	for i in range(4):
		esq = load_image(img1, alpha=True)
		esq = pygame.transform.rotate(esq, i*90)
		lat = load_image(img2, alpha=True)
		lat = pygame.transform.rotate(lat, i*90)
		
		Esquinas.append(esq)
		Laterales.append(lat)
	rectesq = esq.get_rect()	
	rectlat = Laterales[0].get_rect()
	rectlat.top = rectesq.bottom 
	Image = pygame.Surface((width,height), pygame.SRCALPHA, 32)
	Image = Image.convert_alpha()
	
	Image.blit(Esquinas[0], rectesq)
	rectesq.bottom=height
	while rectlat.bottom <= rectesq.top:
		Image.blit(Laterales[0], rectlat)
		rectlat.bottom += 1
		
	rectlat = Laterales[1].get_rect()
	rectlat.top = rectesq.top
	rectlat.left=rectesq.right
	Image.blit(Esquinas[1], rectesq)
	rectesq.right=width
	while rectlat.right <= rectesq.left:
		Image.blit(Laterales[1], rectlat)
		rectlat.right += 1
	
	rectlat = Laterales[2].get_rect()
	rectlat.right = rectesq.right
	rectlat.bottom=rectesq.top	
	Image.blit(Esquinas[2], rectesq)
	rectesq.top = 0
	while rectlat.top >= rectesq.bottom:
		Image.blit(Laterales[2], rectlat)
		rectlat.top -= 1
		
	rectlat = Laterales[3].get_rect()
	rectlat.right = rectesq.left
	rectlat.top=rectesq.top
	Image.blit(Esquinas[3], rectesq)
	rectesq.left = 0
	while rectlat.left >= rectesq.right:
		Image.blit(Laterales[3], rectlat)
		rectlat.left -= 1
		
	rect = pygame.Rect(rectesq.right, rectesq.bottom, width-rectesq.w*2, height-rectesq.h*2)
	pygame.draw.rect(Image, color, rect)
	return Image
		
def ItemsIDs(string):
	IDs=[]
	if "-" in string:
		ind=string.find("-")
		c=int(string[:ind])
		while c<=int(string[ind+1:]):
			IDs.append(c)
			c+=1
	else:
		IDs=string.split(",")
	return IDs
# ---------------------------------------------------------------------
