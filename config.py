#config.py
import pygame, os, sys, random, math, pickle
from pygame.locals import *

# Import Modules
import pygame, sys, time
from pygame.locals import *

from tilemap import *

# Clock
mainclock = pygame.time.Clock()

from textures import *

# Scores
player_money = 20
player_health = 100

# Tower Money Costs
Tower_1 = 5
Tower_2 = 20
Tower_3 = 50
Tower_4 = 100

#Colors for level loading
BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)
GREEN = (100, 255, 100, 255)
BROWN = (124, 66, 0, 255)
WHITE = (255, 255, 255)

# Game Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Barn Defence"
BGCOLOR = GRASS

VISUAL_MAP = TILEMAP

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
