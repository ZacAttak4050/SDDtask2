import sys, os, pygame, math
from config import *
from calculations import *
from main import *
from animals import *
#import widgets

class Tower():
    def __init__(self, screen, x, y, position = (0,0), tower_image = "images/Towers/Tower1.png", frameinterval = 100, template = False):
        Sprite.__init__(self)

        self.name = "Tower 1"
        self.description = None

        if not template:
            game.tower_count += 1
            self.id = game.tower_count
            game.last_placed_tower = self.id
        else:
            self.id = None

        self.type = 'Tower'
        self.screen = screen
        self.game = game
        self.tower_list = None
        if tower_image.__class__ == "".__class__:
            self.image = pygame.image.load(tower_image).convert_alpha()
        elif tower_image.__class__ == [].__class__:
            self.image = pygame.image.load(tower_image[0]).convert_alpha()
            self.tower_list = tower_image
            self.imageframeid = 0
            self.frametimer = Timer(frameinterval, self.next_frame, onetimer = False)

        self.icon = pygame.transform.scale(self.image, (30,30))

        if not template:
            self.coordx_topleft, self.coordy_topleft = self.game.xy2coord(position)
            self.coord_topleft = (self.coordx_topleft, self.coordy_topleft)
            self.pos = game.coord2xy(self.coord_topleft)

        self.cost = 10

        # Statistics or tower
        self.damage = 10
        self.radius = 100
        self.attackspeed = 700 # in milliseconds
        self.last_fired = 0
        self.last_target_id = None

        # Experience for the towers.
        self.level = 1
        self.experience = 0
        self.kills = 0

        # blocking covered tiles from tower placement
        if not template:
            for extra_tile_y in range(int(self.heightbycoord)):
                for extra_tile_x in range(int(self.widthbycoord)):
                    self.game.gridpath.set_blocked((self.coordx_topleft + extra_tile_x, self.coordy_topleft + extra_tile_y))

            self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)

    def draw(self, time_passed):
        if self.tower_list:
            self.frametimer.update(time_passed)
        self.screen.blit(self.image, self.rect)

    def fire(self, target):
        # if the combined time fired and attack speed is less than the total time passed...
        if self.last_fired + self.attackspeed < self.game.total_time_passed:
            last_target = selfgame.lookup_animal(self.last_target_id)
            if self.last_target_id in targets and last_target.state == 0:
                animal_id = self.last_target_id


            else:
                animal_id = choice(targets)

            self.game.attacks += 1
            self.last_fired = self.game.total_time_passed
            self.last_target_id = animal_id

    def next_frame(self):
        if self.imageframeid < len(self.tower_list) - 1:
            self.imageframeid += 1
        else:
            self.imageframeid = 0
        self.image = pygame.image.load(self.tower_list[self.imageframeid]).convert_alpha()

class Tower1(Tower):
    def __init__(self, screen, game, position = (0,0), tower_image = 'images/Towers/Tower1.png', template = False):
        self.name = "Rook Tower"
        self.description = "The Basic Muppet"
        self.cost, template = False
        self.damage = 15
        self.attackspeed = 800

class Tower2(Tower):
    def __init__(self, screen, game, position = (0,0), tower_image  = 'images/Towers/Tower2.png', template = False):
        self.name = "Queen Tower"
        self.description = "Almost there, kinda flawed."
        self.cost = 50
        self.damage = 30
        self.radius - 110
        self.attackspeed = 750

class Tower3(Tower):
    def __init__(self, screen, game, position = (0,0), tower_image = 'images/Towers/Tower3.png', template = False):
        self.name = "Furnace Tower"
        self.description = "Known for its fiery depths."
        self.cost = 75
        self.damage = 50
        self.radius = 120

class Tower4(Tower):
    def __init__(self, screen, game, position = (0,0), tower_image = 'images/Towers/Tower4.png', template = False):
        self.name = "King Tower"
        self.description = "The best of all."
        self.cost = 150
        self.radius = 150
        self.damage = 100
