#tilemap.py

from textures import *

# Constants representing different resources
DIRT = 0
GRASS = 1
WATER = 2
STONE = 3
BLACK = 4

# Constants representing Colour
BROWN = (120, 72, 0)
GREEN = (49, 99, 0)
BLUE = (0, 0, 255)
GREY = (139, 141, 122)
BLACK = (0, 0, 0)

# Dictionary pairing the resources with the colour
colours = {
  DIRT : BROWN,
  GRASS : GREEN,
  WATER : BLUE,
  STONE : GREY,
  BLACK : BLACK
}


tilemap = [
  [GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, WATER, WATER, WATER, GRASS, GRASS, STONE, STONE, STONE, STONE, STONE, STONE, GRASS, GRASS],
  [GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, WATER, WATER, GRASS, GRASS, GRASS, STONE, STONE, STONE, STONE, STONE, STONE, GRASS, GRASS],
  [GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, STONE, STONE, STONE, STONE, GRASS, GRASS, GRASS],
  [GRASS, GRASS, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, GRASS, GRASS, STONE, STONE, STONE, STONE, GRASS, GRASS, GRASS],
  [GRASS, GRASS, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, GRASS, GRASS, GRASS, STONE, STONE, GRASS, GRASS, GRASS, GRASS],
  [GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
  [GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
  [GRASS, GRASS, GRASS, WATER, WATER, STONE, STONE, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, GRASS, STONE, STONE, GRASS, GRASS, GRASS],
  [GRASS, GRASS, WATER, WATER, WATER, STONE, WATER, GRASS, DIRT, DIRT, DIRT, DIRT, DIRT, GRASS, STONE, STONE, GRASS, GRASS, GRASS],
  [GRASS, WATER, WATER, WATER, STONE, STONE, WATER, GRASS, DIRT, DIRT, DIRT, DIRT, DIRT, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
  [GRASS, WATER, WATER, STONE, STONE, WATER, WATER, GRASS, GRASS, GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, WATER, WATER, GRASS],
  [GRASS, STONE, STONE, STONE, WATER, WATER, WATER, WATER, GRASS, GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, WATER, WATER, GRASS],
  [STONE, STONE, WATER, WATER, WATER, WATER, WATER, WATER, GRASS, GRASS, GRASS, DIRT, DIRT, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
  [GRASS, GRASS, GRASS, GRASS, WATER, WATER, WATER, GRASS, GRASS, GRASS, GRASS, DIRT, DIRT, DIRT, DIRT, DIRT, GRASS, GRASS, GRASS],
  [GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, STONE, GRASS, GRASS, DIRT, DIRT, DIRT, DIRT, DIRT, GRASS, GRASS, GRASS],
  [GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BLACK, BLACK, GRASS, GRASS, GRASS]
]