import pygame
from config import *
from main import *
from utils import get_Percentage
import widgets

class animals(Sprite):
    def __init__(self, screen, x, y, level, game, init_position=None, init_direction = (1,1)):
        Sprite.__init__(self)
        self.id = game._spawned_creep_count
        self.screen = screen
        self.game = game
        self.x = x
        self.y = y

        self.type = animals
        self.name = Animalz
        self.speed = random.randint(45,55)/1000.
        self.field = game.field_rect

        animal_images = choice([pygame.image.load(f1).convert_alpha(), pygame.image.load(f2).convert_alpha()) for (f1, f2) in game.ENEMY_FILENAME_LISTS[choice(range(0, len(game.ENEMY_FILENAME_LISTS)))]])

        # This represents the un-rotated animal images.
        self.base_image_0 = animal_images[0]
        #This rotaets the animal images to the direction it was facing.
        self.base_image_45 = animal_images[1]

        # These are the base images for the animals (rotated in game)
        self.image = self.base_image_0
        self.width, self.height = self.image.get_size()

        # These are vectors that specify the position of the animals.
        self.pos = vec2d(init_position)
        self.prev_pos = vec2d(self.pos)
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)

        #direction for normal vectors
        self.direction = vec2d(init_direction).normalized()
        self.state = animals.ALIVE
        self.health_init = 15 * (game_level * 2 + game_level) + int((game.level*1.5)**2)
        self.health = self.health_init

        self.level = game.level
        self.gold = int(round(self.level / 1.99))
        self.damage = 1 # determining the amount of damage the animal does to the base

    def is_alive(self):
        return self.state = (animal.ALIVE)

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Monkey(animals):

# Bear = more health, fox = more lives, frog = hop speed, lizard = basic, monkey, turtle.
