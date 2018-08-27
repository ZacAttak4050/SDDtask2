import pygame, sys, os, math, random
from config import *
from animals import *
from textures import *
from tower import *
from gridmap import GridMap
from pathfinder import PathFinder
from calculations import Timer
from vec2d import vec2d
global menu
from pygame.sprite import Sprite

class Menu(object):
    BCKGROUND = 'images/Textures/dirt.png'
    def __init(self, screen, pause = False, game = None):
        self.background_img = pygame.image.load(self.BCKGROUND).convert_alpha()
        self.screen = screen
        self.pause = pause
        self.game = game
        self.main()
    def main(self):
        self.state = "Main"
        if not self.pause:
            self.screen.blit(self.background_img, (0,0))

        else:
            menutextstring = "Press SPACE to resume game."
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.fill(Color(10, 10, 10))
            overlay.set_alpha(220)
            self.screen.blit(overlay, (0,0))
        self.loop()

    def loop(self):
        self.resume = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT():
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pyagme.K_SPACE:
                        if not self.pause and self.state == "Main":
                            self.run_game()
                        else:
                            self.resume = True
                            break
                if self.state == "Main":
                    if (event.type == self.NEW_GAME_CLICK):
                        self.run_game()
                    elif event.type == self.EXIT_CLICK:
                        self.quit()
            if self.resume == True:
                self.game.paused = False
                break
            pygame.display.flip()

    def run_game(self):
        self.game = Game(self.screen)
        self.game.run()
        del self

    def quit(self):
        pygame.quit()
        sys.exit()

class Game(object):

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    GRID_SIZE = 20
    FIELD_SIZE = 620, 500

    ANIMAL_1 = [
    ('images/Animals/monkey.png')
    ]
    ANIMAL_2 = [
    ('images/Animals/frog.png')
    ]
    ANIMAL_3 = [
    ('images/Animals/turtle.png')
    ]
    ANIMAL_4 = [
    ('images/Animals/fox.png')
    ]
    ANIMAL_5 = [
    ('images/Animals/lizard.png')
    ]
    ANIMAL_6 = [
    ('images/Animals/bear.png')
    ]

    # How many animals per level of the game.
    ANIMALS_PER_LEVEL = 40

    def __init__(self, screen):
        self.screen = screen

        #Statistics
        self.level = 1
        self.kills = 0
        self.attack = 0
        self.player_money = 100
        self.player_health = 100
        self.lose_life = 0
        self.victory = False
        self.tower_count = 0
        self.animal_count = 0
        self.level_complete = False
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.paused = False

        self.money_image = pygame.image.load('images/Textures/money.png').convert_alpha()

        """ Create the grid path representation """
        self.grid_xrows = self.FIELD_SIZE[1] / self.GRID_SIZE
        self.grid_xcols = self.FIELD_SIZE[0] / self.GRID_SIZE
        self.goal_coord = (self.grid_xrows - 1, self.grid_xcols - 1)
        self.gridpath = GridPath(
            xrows = self.grid_xrows,
            xcols = self.grid_xcols,
            goal = self.goal_coord)


        self.options = dict(draw_grid = False)

        self.towers = pygame.sprite.Group()
        self.tower_call_expression_base = "self.towers.add(Tower1(_screen, _game, position = pos))".split('1')
        self.add_animal_expression_base = "self.animals.add(Animal_*(screen = self.screen, game = self))".split('*')

        self.animals = pygame.sprite.Group()
        self.animal_spawn_timer = None
        self.level_timer = Timer(5000, self.next_level, onetimer = True)

    # Designates/Defines when the current level is finished.
    def level_finished(self):
        self.animal_spawn_timer = None
        self.animal_count = 0
        self.level += 1
        self.level_timer = Timer(10000, self.next_level, onetimer = True)
        print("10 seocnds until the next level")

    # When the previous level finishes, this function starts the next level.
    def next_level(self):
        print ("Next Level")
        self.add_animal_expression = ''.join([self.add_animal_expression_base[0], str(self.level), self.add_animal_expression_base[1]])
        self.animal_spawn_timer = Timer(500, self.spawn_new_animal)

    def drawing_place_tower(self, pos):
        Type = self.tower_type
        try:
            image = self.tower_templates[Type[1] - 1].image
        except:
            print("")
            image = pygame.image.load('images/Towers/Tower1.png').convert_alpha()
        place_surface = pygame.Surface((40,40))
        place_surface.set_alpha(150, pygame.RLEACCEL)
        coord = self.xy2coord(pos)
        snap_pos = self.coord2xy(coord)
        place_surface.blit(image, (0,0))
        self.screen.blit(place_surface, snap_pos)
        # This details the font used.
        font = pygame.font.SysFont('calibri', 15)
        font.set_bold(True)
        text = font.render("Press ESC to stop.", True, (0,0,0))
        self.screen.blit(text, (snap_pos[0] + 50, snap_pos[1] + 20))

    # This designates whether the placement of the tower.
    def place_tower(self, pos):
        Type = self.tower_type
        self.place_tower = False
        self.place_tower_pos = None
        self.add_tower = (Type, self.screen, self, pos)

    # This functions adds towers into the game.
    def add_tower(self, Type, screen, game, pos):
        tower_call_expression = ''.join([self.tower_call_expression_base[0], str(Type[1]), self.tower_call_expression_base[1]])
        eval(tower_call_expression)

    # Define which coordinate is next on the path of the animals.
    def next_on_path(self, coord):
        return self.gridpath.get_next(coord)

    def xy2coord(self, pos):
        x, y = (pos[0] - self.field_rect.left, pos[1] - self.field_rect.top)
        return (int(y) / self.GRID_SIZE, int(x) / self.GRID_SIZE)

    def coord2xy(self,coord):
        xrow, xcol = coord
        return (
        self.field_rect.left + xcol * self.GRID_SIZE,
        self.field_rect.top + xrow * self.GRID_SIZE)

    def coord2xy_(self, coord):
        xrow, xcol = coord
        return (self.field_rect.left + xcol * self.GRID_SIZE + self.GRID_SIZE / 2,
                self.field_rect.top + xrow * self.GRID_SIZE + self.GRID_SIZE / 2)

    # The goal coord means the base of the humans/player.
    def reached_goal(self, coord):
        return coord == self.goal_coord

    # This functionis designed to create the spawning of the animals.
    def spawn_new_animal(self):
        if self.animal_spawn_count_level >= self.ANIMALS_PER_LEVEL and not len(self.animals):
            self.level_finished()
            return
        elif self.animal_spawn_count_level >= self.ANIMALS_PER_LEVEL:
            return

        try:
            eval(self.add_animal_expression)
            self.animal_count += 1
            self.animal_spawn_count_level += 1
        except NameError:
            self.victory = True

    def get_field_rect(self):
        return self.field_box.get_internal_rect()

    def get_toolbox_rect(self):
        return self.toolbox.get_internal_rect()

    def lookup_animal(self, animal_id):
        for animal in self.animals:
            if animal.id == animal_id:
                return animal
        return None

    def draw_background(self):
        self.screen.blitz(self.background_img, (0,0))

    def draw_portals(self):
        ANIMAL_BASE = 'images/8 Bit Art/Barn.png'
        self.animal_base = pygame.image.load(self.ANIMAL_BASE).convert_alpha()
        entrance = pygame.Surface((self.entrance_rect.w, self.entrance_rect.h))
        entrance.fill(Color(0,0,0))
        entrance.set_alpha(150)
        self.screen.blit(entrance, self.entrance_rect)

        PLAYER_BASE = 'images/8 Bit Art/logcabin.png'
        self.player_base = pygame.image.load(self.PLAYER_BASE).convert_alpha()
        self.screen.blit(self.player_base, (603,528))

        exit = pygame.Surface((sefl.exit_rect.w, self.exit_rect.h))
        exit.fill(Color(200, 80, 80))
        exit.set_alpha(150)
        self.screen.blit(exit, self.exit_rect)

    def draw_grid(self):
        for y in range(self.grid_xrows + 1):
            pygame.draw.line(
                self.screen,
                Color(50, 50, 50),
                (self.field_rect.left, self.field_rect.top + y * self.GRID_SIZE - 1),
                (self.field_rect.right - 1, self.field_rect.top + y * self.GRID_SIZE - 1))

    def draw(self):
        self.draw_background()
        self.field_box.draw()

        if self.options['draw_grid']:
            self.draw_grid()

        self.screen.blit(self.money_image, (750, 107))
        self.screen.blit(self.fps, (650, 20))

        for tower in self.towers:
            tower.draw()
            if tower == self.selection and self.selection_info_active:
                pygame.draw.circle(self.screen, Color('grey'), tower.rect.center, tower.radius, 2)

        for animal in self.animals:
            animal.draw()

        if self.placing_tower and self.place_tower_pos:
            self.place_tower(self.place_tower_pos)
        self.draw_portals()

    def run(self):
        self.total_time_passed = 0

        while True:
            self.time_passed = self.clock.tick(40)
            self.total_time_passed += self.time_passed
            try:
                self.FPS - 1 / (self.time_passed / 1000.0)
            except:
                self.FPS = 999

            if self.time_passed > 100:
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.game_over:
                            self.paused = not self.paused
                            if self.paused:
                                pausemenu = Menu(self.screen, pause = True, game = self)
                        else:
                            del self
                            menu = Menu(screen)
                    elif event.key == pygame.K_ESCAPE:
                        if self.placing_tower:
                            self.placing_tower = False
                            self.player_money += self.tower_templates[self.placing_tower_type[1] - 1].cost
                            pygame.mouse.set_visible(True)
                    elif event.key == pygame.K_g:
                        if pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.options['draw_grid'] = not self.options['draw_grid']
                    elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                        n = event.key - 48
                        if n in range(1, self.tower_type_amount + 1):
                            self.placing_tower_type = [0,n]
                            if self.placing_tower == False and self.player_money >= self.tower_templates[n - 1].cost:
                                self.placing_tower = True
                            else:
                                self.placing_tower = False

                            if self.placing_tower and self.money >= self.tower_templates[n -1].cost:
                                pygame.mouse.set_visible(False)
                                self.place_tower_pos = pygame.mouse.get_pos()
                                self.placing_tower_type = [0, n]
                                self.playeR_money -= self.tower_templates[self.placing_tower_type[1] - 1].cost

                            else:
                                if self.placing_tower_type == [0,n]:
                                    self.player_money += self.tower_templates[self.placing_tower_type[1] - 1].cost
                                    self.place_tower_pos = None
                                    pygame.mouse.set_visible(True)

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for n in range(1, self.tower_type_amount + 1):
                            if self.get_toolbox_rect_n(n).collidepoint(event.pos) and self.money >= self.tower_templates[n - 1].cost:
                                self.placing_tower = not self.placing_tower
                                if self.placing_tower:
                                    pygame.mouse.set_visible(False)
                                    self.place_tower_draw_pos = pygame.mouse.get_pos()
                                    self.placing_tower_type = [0,n]
                                    self.player_money -= self.tower_templates[self.placing_tower_type[1] - 1].cost
                                else:
                                    self.place_tower_pos = None
                                    pygame.mouse.set_visible(True)

                            else:
                                Collision = None
                                if self.towers:
                                    towers_or_do_once = self.towers
                                else:
                                    towers_or_do_once = range(1)
                                for tower in towers_or_do_once:
                                    if self.towers:
                                        Collision = towe.rrect.collidepoint(event.pos)
                                    if Collision:
                                        self.select(tower)
                                        break

                                    for animal in self.animals:
                                        Collision = animal.rect.collidepoint(event.pos)
                                        if Collision:
                                            self.select(animal)
                                            break
                                    if Collision:
                                        break

                        if not self.paused and not self.game_over:
                            msg1 = 'Animals: %d' % len(self.animals)
                            msg2 = 'Gold: %d' % self.player_money
                            msg3 = 'Lives: %d' % self.player_health
                            msg4 = 'Kills: %d' % self.Kills
                            msg5 = ''

                            if self.player_health <= 0:
                                msg5 = 'GG!'
                                if not self.game_over:
                                    self.GameOver()

                        elif self.victory and self.player_health:
                            msg5 = 'Victory!'
                            if not self.game_over:
                                self.Victory()

                        font = pygame.foont.SysFont('calibri', 24)
                        font.set_bold = True
                        self.fps = font.render('FPS: ' + str(int(self.FPS)), True, (0, 0, 0))


                        self.mboard_text = [msg1, msg2, msg3, msg4, msg5]

                        if not len(self.animals) and self.animal_count >= self.ANIMALS_PER_LEVEL:
                            if self.level_complete = False and self.animal_count >= self.ANIMALS_PER_LEVEL:
                                self.level_complete = True

                            if self.level_timer:
                                self.tboard_text = ['Level ' + str(self.level) + ' Starts in...' + str(int(self.level_timer.interval - self.level_timer.time) / 1000))]

                        else:
                            if self.level_complete == True:
                                self.level_complete = False
                            self.tboard.text = ['Level ' + str(self.level)]

                            if self.animal_spawn_timer:
                                self.animal_spawn_timer.update(self.time_passed)
                            if self.level_timer:
                                self.level_timer.update(self.time_passed)

                            for animal in self.animals:
                                animal.update(self.time_passed)

                            for tower in self.towers:
                                possible_targets = []

                                for animal in self.animmals:
                                    Collision = pygame.sprite.collide_circle(animal, tower)
                                    if Collision and animal.health > 0:
                                        possible_targets.append(animal_id)
                                    if possible_targets:
                                        
