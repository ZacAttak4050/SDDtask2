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
from textmessages import *

class Menu(object):
    BCKGROUND = 'images/Textures/background.jpg'

    NEW_GAME_CLICK = pygame.USEREVENT + 143
    EXIT_CLICK = pygame.USEREVENT + 145

    def __init__(self, screen, pause = False, game = None):
        self.background_img = pygame.image.load(self.BCKGROUND).convert_alpha()
        self.screen = screen
        self.pause = pause
        self.game = game
        self.text_widgets = []
        self.main()

    def main(self):
        self.state = "Main"
        if not self.pause:
            self.screen.blit(self.background_img, (0,0))

            self.new_game_text = TextWidget("Start Game", colour = (0, 100, 0), size = 46, highlight_increase = 12, event = self.NEW_GAME_CLICK)
            self.new_game_text.rect.center = self.screen.get_rect().center
            self.new_game_text.rect.top += 90
            self.new_game_text.rect.left = 70

            self.text_widgets.append(self.new_game_text)

            self.exit_text = TextWidget("Exit Game", colour = (0, 100, 0), size = 46, highlight_increase = 12, event = self.EXIT_CLICK)
            self.exit_text.rect.center = self.screen.get_rect().center
            self.exit_text.rect.top += 140
            self.exit_text.rect.left = 70
            self.text_widgets.append(self.exit_text)

        else:
            menutextstring = "Press SPACE to resume game."
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.fill(Color(10, 10, 10))
            overlay.set_alpha(220)
            self.screen.blit(overlay, (0,0))
            menufont = pygame.font.SysFont('calibri', 30)
            menurect = pygame.Rect(200, 200, 400, 200)
            textsurface = widgets.render_textrect(menutextstring, menufont, menurect, (130, 40, 0), (0,0,0), justificationm = 0)
            self.screen.blit(textsurface, (200, 200))
        self.loop()

    def loop(self):
        self.resume = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pyagme.K_SPACE:
                        if not self.pause and self.state == "Main":
                            self.run_game()
                        else:
                            self.resume = True
                            break
                if self.state == "Main":
                    if (event.type == pygame.ACTIVEEVENT):
                        if (event.gain == 1):
                            for text in self.text_widgets:
                                text.dirty = True
                            self.draw()
                        elif (event.state == 2):
                            # Wait for the next event.
                            pygame.event.post(pygame.event.wait())

                    elif (event.type == pygame.MOUSEMOTION):
                        for text in self.text_widgets:
                            orig = text.highlight
                            text.highlight = text.rect.collidepoint(event.pos)
                            if orig != text.highlight:
                                for t in self.text_widgets:
                                    t.dirty = True
                                self.screen.blit(self.background_img, (0,0))

                    elif (event.type == pygame.MOUSEBUTTONDOWN):
                        for text in self.text_widgets:
                            text.on_mouse_button_down(event)
                            print('GOOD')

                    elif (event.type == pygame.MOUSEBUTTONUP):
                        for text in self.text_widgets:
                            text.on_mouse_button_up(event)
                            print('GOOD')

                    elif (event.type == self.NEW_GAME_CLICK):
                        self.run_game()

                    elif (event.type == self.EXIT_CLICK):
                        self.quit()

            if self.resume == True:
                self.game.paused = False
                break
            self.draw()
            pygame.display.flip()

    def draw(self):
        """ Drawing up the menu screen... text boxes etc. """
        rects = []
        for text in self.text_widgets:
            rect = text.draw(self.screen)
            if (rect):
                rects.append(rect)
        pygame.display.update(rects)

    def run_game(self):
        self.game = Game(self.screen)
        self.game.run()
        print("IT RUNS")
        del self

    def quit(self):
        pygame.quit()
        sys.exit()

class Game(object):

    background_image = 'images/Textures/dirt.png'
    # These are the screen dimensions.
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    # This is the size of each individual grid.
    GRID_SIZE = 20

    FIELD_SIZE = 620, 500

    # This is the directory path for the images of the animals.
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
        self.bck_img = pygame.image.load(self.background_image).convert_alpha()

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

        # These are for the state of the game.
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

        # This is an option for whether or not the player can see the grid representation.
        self.options = dict(draw_grid = False)

        self.towers = pygame.sprite.Group()
        self.tower_call_expression_base = "self.towers.add(Tower1(_screen, _game, position = pos))".split('1')
        self.add_animal_expression_base = "self.animals.add(Animal_*(screen = self.screen, game = self))".split('*')

        # Creates the group of animals as well as the very first animal to come.
        self.animals = pygame.sprite.Group()
        self.animal_spawn_timer = None
        self.level_timer = Timer(5000, self.next_level, onetimer = True)

    def level_finished(self):
        """ Determines what happens when the level finishes. """
        self.animal_spawn_timer = None # Stops animal spawning.
        self.animal_count = 0 # Occurs when the amount of animals is 0.
        self.level += 1 # moves onto the next level.
        self.level_timer = Timer(10000, self.next_level, onetimer = True) # In ms...
        print("10 seocnds until the next level")

    def next_level(self):
        """ Determines what happens for the next level. """
        print ("Next Level")
        self.add_animal_expression = ''.join([self.add_animal_expression_base[0], str(self.level), self.add_animal_expression_base[1]])
        self.animal_spawn_timer = Timer(500, self.spawn_new_animal)

    def drawing_place_tower(self, pos):
        """ Draws the tower when the player is deciding where to place it. """
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

    def place_tower(self, pos):
        """ Designates where the placement of the tower is. """
        Type = self.tower_type
        self.place_tower = False
        self.place_tower_pos = None
        self.add_tower = (Type, self.screen, self, pos)

    def add_tower(self, Type, screen, game, pos):
        """ Function adds the towers into the game. """
        tower_call_expression = ''.join([self.tower_call_expression_base[0], str(Type[1]), self.tower_call_expression_base[1]])
        eval(tower_call_expression)

    def next_on_path(self, coord):
        """ Define where the next coordinate or path of the animal is. """
        return self.gridpath.get_next(coord)

    def xy2coord(self, pos):
        """ This converts an (x, y) pair to a (xrow, xcol) coordinate. """
        x, y = (pos[0] - self.field_rect.left, pos[1] - self.field_rect.top)
        return (int(y) / self.GRID_SIZE, int(x) / self.GRID_SIZE)

    def coord2xy(self,coord):
        """ Converts a (xrow, xcol) coordinate to an (x, y) coordinate. """
        xrow, xcol = coord
        return (
        self.field_rect.left + xcol * self.GRID_SIZE,
        self.field_rect.top + xrow * self.GRID_SIZE)

    def middle_of_coord2xy(self, coord):
        """ This converts a (xrow, xcol) coordinate to a (x, y) coordinate where the (x, y)
            is in the middle of the square (coord).
        """
        xrow, xcol = coord
        return (self.field_rect.left + xcol * self.GRID_SIZE + self.GRID_SIZE / 2,
                self.field_rect.top + xrow * self.GRID_SIZE + self.GRID_SIZE / 2)

    def reached_goal(self, coord):
        """ Determines whether the animal has reached the base of the player. """
        return coord == self.goal_coord

    def spawn_new_animal(self):
        """ This function is focused around the spawning of the animals. """
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

    def lookup_animal(self, animal_id):
        for animal in self.animals:
            if animal.id == animal_id:
                return animal
        return None

    def draw_background(self):
        TILESIZE = 32

        self.screen.blit(self.bck_img, (0,0))

    def draw_portals(self):
        """ This is to draw up the entrances/exits of the animals, or known as
            the bases of the animals and the player.
        """
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
        """ This function draws the gridmap of the game which allows for the player
            to easily place towers.
        """

        for y in range(self.grid_xrows + 1):
            pygame.draw.line(
                self.screen,
                Color(50, 50, 50),
                (self.field_rect.left, self.field_rect.top + y * self.GRID_SIZE - 1),
                (self.field_rect.right - 1, self.field_rect.top + y * self.GRID_SIZE - 1))

    def draw(self):
        """ This function is to draw up all the other functions. """

        self.draw_background()

        if self.options['draw_grid']:
            self.draw_grid() # Draws up the grid.

        self.screen.blit(self.money_image, (750, 107)) # This is the money image.
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
        """ This functions runs the game. Otherwords, the main game loop. """

        self.total_time_passed = 0

        while True:
            # Limits the speed to 30 FPS.
            self.time_passed = self.clock.tick(40) # FPS
            self.total_time_passed += self.time_passed
            try:
                self.FPS - 1 / (self.time_passed / 1000.0)
            except:
                self.FPS = 999
                # This si to determine whether too long has passed between two frames.
                # If it has, don't update (the game must've been suspended).

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

                            if self.placing_tower and self.money >= self.tower_templates[n - 1].cost:
                                pygame.mouse.set_visible(False)
                                self.place_tower_pos = pygame.mouse.get_pos()
                                self.placing_tower_type = [0, n]
                                self.player_money -= self.tower_templates[self.placing_tower_type[1] - 1].cost

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
                            """ This is for the player statistics/board, which
                                hasn't been created yet.
                            """

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

                        font = pygame.font.SysFont('calibri', 24)
                        font.set_bold = True
                        self.fps = font.render('FPS: ' + str(int(self.FPS)), True, (0, 0, 0))


                        #self.mboard_text = [msg1, msg2, msg3, msg4, msg5]

                        if not len(self.animals) and self.animal_count >= self.ANIMALS_PER_LEVEL:
                            if self.level_complete == False and self.animal_count >= self.ANIMALS_PER_LEVEL:
                                self.level_complete = True

                            #if self.level_timer:
                                #self.tboard_text = ['Level ' + str(self.level) + ' Starts in...' + str(int(self.level_timer.interval - self.level_timer.time) / 1000)]

                        else:
                            if self.level_complete == True:
                                self.level_complete = False
                            #self.tboard.text = ['Level ' + str(self.level)]

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
                                    tower.fire(possible_targets)
                            if not self.game_over:
                                self.draw()
                                pygame.display.flip()

    def Victory(self):
        self.game_over = True
        self.paused = True
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill(Color(100,10,10))
        overlay.set_alpha(220)
        self.screen.blit(overlay, (0,0))
        widgets.Textmessage(self.screen, "Victory!", vec2d(self.screen.get_width() / 2, (self.screen.get_height() / 2)+ 50), duration = 0, size = 32, flashy = False).draw()
        pygame.display.flip()

    def GameOver(self):
        self.game_over = True
        self.paused = True
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill(Color(100, 10, 10))
        overlay.set_alpha(220)
        self.screen.blit(overlay, (0,0))
        widgets.Textmessage(self.screen, "Game Over!", vec2d(self.screen.get_width() / 2, (self.screen.get_height() / 2)+50), duration = 0, size = 32, flashy = False).draw()
        pygame.display.flip()

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    pygame.init()
    global screen
    while 1:
        screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)
        pygame.display.set_caption('Barn Defence')
        menu = Menu(screen)
