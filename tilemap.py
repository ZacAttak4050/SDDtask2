
#tilemap.py
#from textures import *
import pygame, sys, os

pygame.init()

#Screen Parameters
SCREEN = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Barn Defense')

# Constants representing different resources
DIRT = 0
GRASS = 1
WATER = 2
STONE = 3
BLACK = 4

TILESIZE = 32
column = 5
row = 7

# Constants representing Colour
BROWN = (120, 72, 0)
GREEN = (49, 99, 0)
BLUE = (0, 0, 255)
GREY = (139, 141, 122)
BLACK = (0, 0, 0)

#pygame.display.flip
pygame.draw.rect(SCREEN, GREEN, (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    SCREEN.fill((49, 99, 0))
  pygame.display.update()

  def TileMap(object):
      DIRT = 0
      GRASS = 1
      WATER = 2
      STONE = 3
      BLACK = 4

      TILESIZE = 32
      COLUMN = 5
      ROW = 7

      BROWN = (120, 72, 0)
      GREEN = (49, 99, 0)
      BLUE = (0, 0, 255)
      GREY = (139, 141, 122)
      BLACK = (0, 0, 0)

      def __init__(self):
          pygame.draw.Rect()
