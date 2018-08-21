import sys, os, pygame, math
from config import *
from calculations import *
from main import *
from animals import *
import widgets

class Tower(Sprite):
    def __init__(self, screen, x, y, position = (0,0), tower_image = "images/Towers/Tower1.png", frameinterval = 100, template = False):
        Sprite.__init__(self)

        self.name = "Tower 1"
        self.description = None

        if not template:
            game.tower_count += 1
            self.id = game.tower_count
            game.last_placed_tower = self.id
            
