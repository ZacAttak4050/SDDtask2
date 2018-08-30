
#tilemap.py
#from textures import *
import pygame, sys, os

pygame.init()

#Screen Parameters
SCREEN = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Barn Defense')

TILESIZE = 32
column = 5
row = 7

#pygame.display.flip
pygame.draw.rect(SCREEN, (69, 132, 7), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    SCREEN.fill((69, 132, 7))
  pygame.display.update()
