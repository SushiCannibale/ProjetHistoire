import pygame as pg
import utils

class Button:
    def __init__(self, surface, text, size, pos, text_color, back_color, align, fontname):
        self.surface = surface
        self.text = text
        self.size = size
        self.pos = pos
        self.text_color = text_color
        self.back_color = back_color
        self.align = align
        self.fontname = fontname

        self.rect = utils.get_rect_from_text(text, size, fontname)
        if align in ('left', 'l'):
            self.rect.topleft = pos
        else:
            self.rect.center = pos

    def draw(self):
        utils.draw_text(self.surface, self.text, self.size, self.pos, self.text_color, self.align, self.fontname)

    def draw_back(self, *args):
        pg.draw.rect(self.surface, self.back_color, self.rect, *args)