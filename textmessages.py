import os, sys, random

import pygame
from pygame import Rect, Color
from pygame.locals import *

class WidgetError(Exception): pass
class LayoutError(WidgetError): pass

class MessageBoard(object):
    """ A rectangular "board" for displaying messages on the
        screen. Uses a Box with text drawn inside.

        The text is a list of lines. It can be retrieved and
        changed with the .text attribute.
    """
    def __init__(self,
            surface,
            rect,
            text,
            font=('arial', 20),
            font_color=Color('white'),
            bgcolor=Color('gray25'),
            border_width=0,
            border_color=Color('black'),
            tooltip=False,
            game=None,
            alpha=255):
        """ rect, bgcolor, border_width, border_color have the
            same meaning as in the Box widget.

            text:
                The initial text of the message board.
            font:
                The font (a name, size tuple) of the message
            font_color:
                The font color
        """
        self.surface = surface
        if game and tooltip:
            self.rect = game.mboard.rect #Rect(660, 440, 120, 130)  #game.get_toolbox_rect()#game.get_toolbox_rect_n(game.tooltip_id) ### FIXME
        else:
            self.rect = rect
        self.text = text
        self.bgcolor = bgcolor
        self.font = pygame.font.SysFont(*font)
        self.font_color = font_color
        self.border_width = border_width

        if tooltip:
            self.active = False #default
            self.alpha = 200
        else:
            self.active = True
            self.alpha = False
        self.alpha = alpha
        self.box = Box(surface, self.rect, bgcolor, border_width, border_color, alpha=self.alpha)#, alpha=self.alpha)
    def update(self, rect):
        self.rect = rect
        self.box.update(rect)

    def draw(self):
        self.box.draw()

        # Internal drawing rectangle of the box
        #

        text_rect = Rect(
            self.rect.left + self.border_width,
            self.rect.top + self.border_width,
            self.rect.width - self.border_width * 2,
            self.rect.height - self.border_width * 2)

        x_pos = text_rect.left
        y_pos = text_rect.top

        # Render all the lines of text one below the other
        #
        for line in self.text:
            line_sf = self.font.render(line, True, self.font_color)#, self.bgcolor)

            if (    line_sf.get_width() + x_pos > self.rect.right or
                    line_sf.get_height() + y_pos > self.rect.bottom):
                raise LayoutError('Cannot fit line "%s" in widget' % line)

            self.surface.blit(line_sf, (x_pos, y_pos))
            y_pos += line_sf.get_height()

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0): #From http://www.pygame.org/pcr/text_rect/index.php
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    import pygame

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise (TextRectException, "The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise (TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise (TextRectException, "Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface

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

        self.xdirection = random.choice([-1, 1])

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

    TEXT_WIDGET_CLICK = pygame.locals.USEREVENT

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


    def create_font(self):
        if (self.size):
            try:
                self.__m_font = pygame.font.Font(self.font_filename, self.size)

            except (Exception, e):
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

class Box(object):
    def __init__(self, surface, rect, bgcolor, border_width = 0, border_color = Color('black'), alpha = False):
        # Rect defines the location and size of the box on the surface.
        self.surface = surface
        self.rect = rect
        self.bgcolor = bgcolor
        self.border_width = border_width
        self.border_color = border_color
        self.alpha = alpha

        self.in_rect = Rect(
            self.rect.left + self.border_width,
            self.rect.top + self.border_width,
            self.rect.width - self.border_width * 2,
            self.rect.height - self.border_width * 2)

    def update(self, rect):
        self.rect = rect
        self.in_rect = Rect(
            self.rect.left + self.border_width,
            self.rect.top + self.border_width,
            self.rect.width - self.border_width * 2,
            self.rect.height - self.border_width * 2)

    def draw(self):
        """ Draws up the box """
        box_border = pygame.Surface((self.rect.w, self.rect.h))
        box_border.fill(self.border_color)
        box_background = pygame.Surface((self.in_rect.w, self.in_rect.h))
        box_background.fill(self.bgcolor)
        if self.alpha:
            box_border.set_alpha(self.alpha)
            box_background.set_alpha(self.alpha)

        self.surface.blit(box_border, self.rect)
        self.surface.blit(box_background, self.in_rect)

    def get_internal_rect(self):
        return self.in_rect

if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    box = Box(screen, Rect(20, 20, 40, 40), Color('brown4'), 0, Color('red'))
    mb = MessageBoard(screen, Rect(80, 100, 200, 55), ["Bozo", "Jogd"], border_width = 2, border_color = Color('yellow'), font = ('calibri', 16))

    while True:
        time_passed = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        box.draw()
        mb.draw()

        pygame.display.flip()
