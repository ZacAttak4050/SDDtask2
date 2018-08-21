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

        animal_images = choice([pygame.image.load(f1).convert_alpha(), pygame.image.load(f2).convert_alpha()) for (f1, f2) in game.ANIMAL_FILENAME_LISTS[choice(range(0, len(game.ANIMAL_FILENAME_LISTS)))]])

        # This represents the un-rotated animal images.
        self.base_image_0 = animal_images[0]
        # This rotates the animal images to the direction it was facing.
        self.base_image_45 = animal_images[1]

        # These are the base images for the animals (rotated in game)
        self.image = self.base_image_0
        self.width, self.height = self.image.get_size()

        # These are vectors that specify the position of the animals.
        self.pos = vec2d(init_position)
        self.prev_pos = vec2d(self.pos)
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)

        # direction for normal vectors
        self.direction = vec2d(init_direction).normalized()

        # These represent the animals 'statistics'
        self.state = animals.ALIVE
        self.health_init = 15 * (game_level * 2 + game_level) + int((game.level*1.5)**2)
        self.health = self.health_init

        self.level = game.level
        self.gold = int(round(self.level / 1.99))
        self.damage = 1 # determining the amount of damage the animal does to the base

    def is_alive(self):
        return self.state = (animal.ALIVE, animal.DEAD)

    # This continuously updates the animals throughout the player's game.
    def update(self, time_passed):
        if self.state == animal.ALIVE:
            self._compute_direction(time_passed)

            if int(round(self.direction.angle)) % 90 == 45:
                self.image = pygame.transferm.rotate(
                    self.base_image_45, -(self.direction.angle + 45))
            elif int(round(self.direction.angle)) % 90 == 0:
                self.base_image_0, -(self.direction.angle)
            else:
                assert False

            # This is represents the movement of the animals.
            displacement = vec2d(
            self.direction.x * self.speed * time_passed,
            self.direction.y * self.speed * time_passed)

            self.prev_pos = vec2d(self.pos)
            self.pos += displacement

            self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)

            self.image_w, self.image_h = self.image.get_size()
            self.image_rect = Rect(self.pos[0], self.pos[1], self.width, self.height)

        # When the animal is dead, the entity disappears (no animation)
        elif self.state == animal.DEAD:
            self.__die()

    # Blitting the animals onto the constructed screen.
    def draw(self):
        if self.state == animal.ALIVE:
            # The animal image is placed at self.pos, allowing for smoother
            # movement even when rotated.
            self.draw_rect = self.image.get_rect().move(
            self.pos.x - self.image_w / 2,
            self.pos.y - self.image_h / 2
            self.screen.blit(self.image, self.draw_rect)

            # Visual aspects of the health bar (10x4 px)
            health_bar_length = 10
            health_bar_height = 4

            health_percentage = get_Percentage(self.health.init, self.heatlh)

            health_bar_fill_length = int(cell(health_percentage * health_bar_length))
            health_bar_x = self.pos.x - floor(health_bar_length / 2) + 1
            health_bar_y = (self.pos.y - self.image_h / 2) - floor(health_bar_length / 2) - 1
            self.screen.fill( Color('red'),
                (health_bar_x, health_bar_y, health_bar_length, health_bar_height))
            self.screen.fill( Color('green'),
                                (   health_bar_x, health_bar_y,
                                    health_bar_fill_length, health_bar_height))

        elif self.state == animal.DEAD:
            pass

    # Defining what statest the animals can be in.
    #
    # ALIVE = moving on the screen.
    # DEAD = inactive
    #
    (ALIVE, DEAD) = range(2)

    # This defines what happens when the animal dies.
    # The total kill count is incremented by 1
    # The player's money count is increased by self.gold which is defined previously.
    # A text message appears to inform the player of this.
    def _die(self):
        self.state = animal.DEAD
        self.game.kills += 1
        self.game.player_money += self.gold
        self.game.text_messages.append(widgets.TextMessage(self.game.screen, '+'+str(self.gold), vec2d(self.pos[0], self.pos[1] - 22, duration=1100, size=15))

    # This informs the player if an animal reaches the base.
    # The player loses self.damage lives.
    def _loselife(self):
        self.game.text_messages.append(widgets.TextMessage(self.screen, "-1", self.pos, duration=2000, size=14, initialdelay = 400, color = (245,15,15)))
        self.game.lose += self.damage
        self.game.lives -= self.damage
        self.kill() # This kills the animals once it reaches the player's base.

    # This determines where the animals go.
    def _compute_direction(self, time_passed):
        coord = self.game.xy2coord(self.pos)
    # The animal asks the GAme where it has to go, and it has reached the goal
    # The animal leaves the game.
        if self.game.is_gaol_coord(coord):
            self._loselife() # Removes one life and dies.
        else:
            x_mid, y_mid = self.game.coord2xy_mid(coord)

            if ((x_mid - self.pos.x) * (x_mid - self.prev_pox.s) < 0 or
                (y_mid - self.pos.y) * (y_mid - self.prev_pos.y) < 0):

                success = False
                for n in range(0, 900):
                    try:
                        next_coord = self.game.next_on_path(coord)
                        self.direction = vec2d(
                            next_coord[1] - coord[1],
                            next_coord[0] - coord[0]).normalized()
                        break # This means the path is good to go.
                    except:
                        self.game.placed_tower(self.game.last_placed_tower_id - n).sell()
                        self.game.text_messages.append(widgets.TextMessage(self.game.screen, "Don't block the path!", vec2d(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2, duration = 3000, size = 32, initialdelay = 1000, color = Color("red")))

    def _point_is_inside(self, point):
        # This answers whether a given point is within the animal's body
        # By answering this question, it prevents further problems.

        img_point = point - vec2d(
            int(self.pos.x - self.image_w / 2),
            int(self.pos.y - self.image_h / 2))

        try:
            pix = self.image.get_at(img_point)
            return pix[3] > 0

        except IndexError:
            return False

    def _decrease_health(self, n, attacker = None):
        self.health = max(0, self.health - n)
        if self.health == 0
            if animal_fighter and self.state == animal.ALIVE:
                animal_fighter.tower.add_experience(self.level)
            self._die()

# GridPath is sourced from the GridMap.
class GridPath(object):
    def __init__(self, xrows, xcols, end):
        self.map = GridMap(xrows, xcols)
        # the 'end' is the base of the humans.
        self.end = end
        self._path_cache = {}

    def get_next_coordinate(self, coord):
        # Gets the next coordinate for movement towards the goal
        if not (coord in self._path_cache):
            self._compute_path(coord)
        # By adding a cache, it prevents re-computing of the same coordinates
        # over and over again.
        if coord in self._path_cache:
            return self._path_cache[coord]
        else:
            return None

    def _compute_path(self, coord):
        finder = Path(self.map.successors, self.map.move_cost, self.map.move_cost)
        path_list = list(finder.compute_path(coord, self.end))

        # Enumerate allows for a continuous loop and an automatic counter.
        for i, path_coord in enumerate(path_list):
            next_i = i if i == len(path_list) - 1 else + 1
            self._path_cache[path_coord] = path_list[next_i]

# The monkey is the basic unit.
class Monkey(animals):
    def __init__(self, screen, game, init_position = None, init_direction = (1,1)):
        animals.__init__(self, screen, game, init_position, init_direction):
        self.name = "Monkey"
        self.speed = random.randint(45,55)/1000

# The turtle is the slow tank.
class Turtle(animals):
    def __inti__(self, screen, game, init_position = None, init_direction = (1,1)):
        animals.__init__(self, screen, game, init_position, init_direction):
        self.name = "Turtle"
        self.health_init += 1000
        self.health += 1000
        self.speed = random.randint(20,30)/1000

# The bear is the fast tank, the boss.
class Bear(animals):
    def __init__(self,screen, game, init_position = None, init_direction = (1,1)):
        animals.__init__(self, screen, game, init_position, init_direction):
        self.name = "Bear"
        self.health_init += 2000
        self.health += 2000
        self.speed = random.randint(45,55)/1000

# The frog is the faster type of animal.
class Frog(animals):
    def __init__(self, screen, game, init_position = None, init_direction = (1,1)):
        animals.__init__(self, screen, game, init_position, init_direction):
        self.name = "Frog"
        self.health_init += 50
        self.health_init += 50
        self.speed = random.randint(65,75)/1000

class Fox(animals):
    def __init__(self, screen, game, init_position = None, init_direction = (1,1)):
        animals.__init__(self, screen, game, init_position, init_direction):
        self.name = "Fox"
        self.health_init += 90
        self.health_init += 90
        self.speed = random.randint(50,60)/1000

class Lizard(animals):
    def __init__(self, screen, game, init_position = None, init_direction = (1,1)):
        animals.__init__(self, screen, game, init_position, init_direction):
        self.name = "Lizard"
        self.health_init += 40
        self.health_init += 40
        self.speed = random.randint(70,80)/1000
