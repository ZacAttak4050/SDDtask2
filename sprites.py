import pygame
from config import *

class animals(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.image.load('images/Animals/monkey.png')
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
