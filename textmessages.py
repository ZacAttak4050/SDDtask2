import os, sys, random, math, pygame

import pygame
from pygame import Rect, Color
from pygame.locals import *

class Textmessage(object):
    def __init__(self, screen, text, pos, duration = 1000, size = 12, flashy = True, initialdelay = 200, color = Color(34, 139, 34)):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont('calibri', self.size)
        self.font.set_bold = True
        self.textstring = Text
        self.text = self.font.render(text, True, color)
        self.duration = duration
        self.initialdelay = initialdelay
        self.flashy = flashy
        self.timeon = 0
        self.lastactiontime = 0
        if duration > 0:
            self.sizereduction_peraction = ((size / 1.9) / duration) * 50.
            if self.sizereduction_peraction >= 0.5 or self.sizereduction_peraction <= 1:
                self.sizereduction_peraction = 1
            else:
                self.sizereduction_peraction = round(self.sizereduction_peraction)

        self.xdirectionm = random.choice([-1, 1])

    def update(self, time_passed):
        self.timeon += time_passed
        if self.timeon - 200 > self.lastactiontime and self.flashy and self.timeon > self.initialdelay:
            self.pos[1] -= 4
            self.pos[0] += 2 * self.xdirection
            self.size -= self.sizereduction_peraction
            self.font = pygae.font.SysFont('calibri', self.size)
            self.font.set_bold = True
            self.text = self.font.render(self.textstring, True, self.color)

    def draw(self):
        self.screen.blit(self.text, (self.pos[0] - (self.text.get_width() / 2) , self.pos[1] - (self.text.get_height() / 2)))

class TextWidget(object):
    """ Class to handle texts in my PyGame; this is for things such as the Menu.
        It performs the basic functions such as highlighting and signifying whether
        a button or text has been clicked.
    """

    TEXT_WIDGET_CLICK = pygame.USEREVENT + 143

    __hand_cursor_string = (
    "     XX         ",
    "    X..X        ",
    "    X..X        ",
    "    X..X        ",
    "    X..XXXXX    ",
    "    X..X..X.XX  ",
    " XX X..X..X.X.X ",
    "X..XX.........X ",
    "X...X.........X ",
    " X.....X.X.X..X ",
    "  X....X.X.X..X ",
    "  X....X.X.X.X  ",
    "   X...X.X.X.X  ",
    "    X.......X   ",
    "     X....X.X   ",
    "     XXXXX XX   ")

    __hcurs, __hmask = pygame.cursors.compile(__hand_cursor_string, ".", "X")
    __hand = ((16, 16), (5, 1), __hcurs, __hmask)

    def __get_text(self):
        return self.__m_text
    def __set_text(self, text):
        if (self.__m_text != text):
            self.__m_text = text
            self.update_surface()
    def __del_text(self):
        del self.__m_text
    def __doc_text(self):
        return "The text to be displayed by the text widget."
    text = property(__get_text, __set_text, __del_text, __doc_text)

    def __get_colour(self):
        return self.__m_colour

    def __set_colour(self, colour):
        if (self.__m_colour != colour):
            self.__m_colour = colour
            self.update_surface()
    colour = property(__get_colour, __set_colour)

    def __get_size(self):
        return self.__m_size

    def __set_size(self, size):
        if (self.__m_size != size):
            self.__m_size = size
            self.create_font()
    size = property(__get_size, __set_size)

    def __get_font_filename(self):
        return self.__m_font_filename

    def __set_font_filename(self, font_filename):
        if (self.__m_font_filename != font_filename):
            self.__m_font_filename = font_filename

            if (not os.access(self.__m_font_filename, os.F_OK)):
                self.__m_font_filename = os.path.join(self.__local_path, self.__m_font_filename)

            self.create_font()

    font_filename = property(__get_font_filename, __set_font_filename)

    def __get_highlight(self):
        return self.__m_highlight

    def __set_highlight(self, highlight):
        if (not(self.__m_highlight == highlight)):

            if (self.__m_highlight):
                self.bold_rect = self.rect
            self.__m_highlight = highlight

            self.update_cursor()

            if (highlight):
                self.size += self.highlight_increase
            else:
                self.size -= self.highlight_increase
            if (self.highlight_increase == 0):
                self.create_font()
    highlight = property(__get_highlight, __set_highlight)

    def __get_highlight_cursor(self):
        return self.__m_highlight_cursor

    def __set_highlight_cursor(self, highlight_cursor):
        if (self.__m_highlight_cursor != highlight_cursor):
            self.__m_highlight_cursor = highlight_cursor
            self.update_cursor()
    highlight_cursor = property(__get_highlight_cursor, __set_highlight_cursor)


    def __init__(self, text = "", colour = (0, 0, 0), size = 32, highlight_increase = 20, font_filename = None, show_highlight_cursor = True, event = TEXT_WIDGET_CLICK):
        self.dirty = False
        self.bold_rect = None
        self.highlight_increase = highlight_increase
        self.tracking = False
        self.rect = None
        self.event = event

        self.__local_path = os.path.realpath(os.path.dirname(__file__))

        self.__m_font = None
        self.__m_text = None
        self.__m_colour = None
        self.__m_size = None
        self.__m_font_filename = None
        self.__m_highlight = False
        self.__m_highlight_cursor = False
        self.__m_rect = None

        self.text = text
        self.colour = colour
        self.size = size
        self.font_filename = font_filename
        self.highlight = False
        self.highlight_cursor = show_highlight_cursor

        self.create_font()

    def __str__(self):
        return "TextWidget: %s at %s" % (self.text, self.rect)

    def update_cursor(self):
        if (self.highlight_cursor):
            if (self.highlight):
                pygame.mouse.set_cursor(*self.__hand)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def Exception(self):
        pass

    def create_font(self):
        if (self.size):
            try:
                self.__m_font = pygame.font.Font(self.font_filename, self.size)

            except e:
                print("Error creating font: '%s' using file '%s'" % (
                    str(e), self.font_filename))
                print("Trying with default font")
                self.__m_font = pygame.font.Font(None, self.size)

            self.update_surface()

    def update_surface(self):
        if (self.__m_font):
            self.__m_font.set_bold(self.highlight)
            self.image = self.__m_font.render(self.text, True, self.colour)
            self.dirty = True
            if (self.rect):
                self.rect = self.image.get_rect(center = self.rect.center)
            else:
                self.rect = self.image.get_rect()

    def draw(self, screen):

        rect_return = None
        if ((self.image) and (self.rect) and (self.dirty)):
            if (self.bold_rect):
                rect_return = pygame.Rect(self.bold_rect)
                self.bold_rect = None
            else:
                rect_return = self.rect

            screen.blit(self.image, self.rect)

            self.dirty = False

            return rect_return

    def on_mouse_button_down(self, event):
        self.tracking = False
        if (self.rect.collidepoint(event.pos)):
            self.tracking = True

    def on_mouse_button_up(self, event):
        if ((self.tracking) and (self.rect.collidepoint(event.pos))):
            self.tracking = False
            self.on_mouse_click(event)

    def on_mouse_click(self, event):
        event_attribute = {}
        event_attribute["button"] = event.button
        event_attribute["pos"] = event.pos
        event_attribute["text_widget"] = self
        e = pygame.event.Event(self.event, event_attribute)
        pygame.event.post(e)

if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pygame.display.flip()
