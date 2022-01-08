import pygame as pg
from utils import utils


class Button:
    def __init__(self, surface, text, size, pos, color, align, fontname, offsetx=10, offsety=5, active_func=None):
        self.surface = surface
        self.text = text
        self.size = size
        self.pos = pos
        self.color = color
        # text color
        self.align = align
        self.fontname = fontname
        # text's font
        self.active_func = active_func
        # function called whenever button is clicked

        rect = utils.get_rect_from_text(text, size, fontname)
        if align in ('left', 'l'):
            rect.midleft = pos
        elif align in ('right', 'r'):
            rect.midright = pos
        elif align in ('up', 'u'):
            rect.midtop = pos
        elif align in ('down', 'd'):
            rect.midbottom = pos
        else:
            rect.center = pos

        self.rect = pg.Rect(rect.x - offsetx, rect.y - offsety, rect.w + 2*offsetx, rect.h + 2*offsety)
        # adds the offset to the rect

    def draw(self):
        utils.draw_text(self.surface, self.text, self.size, self.pos, self.color, self.align, self.fontname)

    """ 0 -> idle ; 1 -> hovered ; 2 -> pressed """
    def state(self):
        mx, my = pg.mouse.get_pos()
        if self.rect.x <= mx <= self.rect.x + self.rect.w and self.rect.y <= my <= self.rect.y + self.rect.h:
            if pg.mouse.get_pressed()[0]:
                return 2
            return 1
        return 0

    def draw_back(self, back_color, *args):
        pg.draw.rect(self.surface, back_color, self.rect, *args)