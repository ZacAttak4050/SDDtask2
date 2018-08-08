import pygame as pg
from os import path
import sys
from pygame.locals import *

# Initialise all packages.
pg.init()

# Display values
display_height = 800
display_width = 600

# Load textures needed for the game
water_tile = pg.image.load(path.join('images/Textures/water.png'))
dirt_tile = pg.image.load(path.join('images/Textures/dirt.png'))
stone_tile = pg.image.load(path.join('images/Textures/stone.png'))
grass_tile = pg.image.load(path.join('images/Textures/grass.png'))

#Constants for tiles
water = 0
dirt = 1
stone = 2
grass = 3

# Linking Textures
textures = {
    water : water_tile,
    dirt : dirt_tile,
    stone : stone_tile,
    grass : grass_tile
    }

tilemap = [
    
    [water, dirt, stone, grass],
    [water, dirt, stone, grass],
    [water, dirt, stone, grass]

    ]

TILESIZE = 32
MAPWIDTH = 5
MAPHEIGHT = 3

screen = pg.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        screen.fill((255,0,0));
        for row in range(MAPWIDTH):
            print
            for column in range(MAPHEIGHT):
                screen.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

pygame.display.update()

                
#class TileMap():
  #  def __init__(self, screen, game, position = (0,0), tile_image='images/Textures/dirt.png')
    #screen = pygame.display.set_mode((display_height, display_width))
    
    
