import pygame as pg

from utils.configs import *
import utils.utils
from menus.buttons import Button

class Menu:
    def __init__(self, game):
        self.game = game
        self.doDisplay = False
        self.corner_imgs = []

        for i in range(0, 360, 90):
            img = pg.image.load('src/assets/props/menu_corner.png')
            rescaled = pg.transform.scale(img, (128, 128))
            rotated = pg.transform.rotate(rescaled, i)
            self.corner_imgs.append(rotated)

    def draw_corners(self):
        self.game.screen.blit(self.corner_imgs[0], (10, 10))
        self.game.screen.blit(self.corner_imgs[1], (10, HEIGHT-128-10))
        self.game.screen.blit(self.corner_imgs[2], (WIDTH-128-10, HEIGHT-128-10))
        self.game.screen.blit(self.corner_imgs[3], (WIDTH-128-10, 10))


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        def trigger_play():
            self.doDisplay, self.game.isPlaying = False, True

        def trigger_options():
            print("Options")

        self.btn_start = Button(self.game.screen, "Start", 32, [WIDTH//2, HEIGHT//2], pg.Color("white"), 'c', SSCR, offsetx=40, offsety=8, active_func=trigger_play)
        self.btn_options = Button(self.game.screen, "Options", 32, [WIDTH//2, HEIGHT//2 + 64], pg.Color("white"), 'c', SSCR, offsetx=40, offsety=8, active_func=trigger_options)
        self.allButtons = [self.btn_start, self.btn_options]

    def display(self):
        self.doDisplay = True
        while self.doDisplay:
            self.game.events()
            self.game.refreshDisplay()
            self.draw()

            pg.display.flip()


    def draw(self):
        self.draw_corners()
        utils.utils.draw_text(self.game.screen, "Projet d'Histoire - La Résistance", 64, (WIDTH//2, 128), pg.Color("white"), 'c', ALKHEM)
        for btn in self.allButtons:
            state = btn.state()
            if state == 1:
                btn.draw_back(pg.Color("gray9"), 0, 100)
            elif state == 2:
                btn.draw_back(pg.Color("gray10"), 0, 100)
                btn.active_func() # triggers the button's function
            btn.draw()

        utils.utils.draw_text(self.game.screen, "Théodule & Marc-Aurèle - TG4", 24, (WIDTH//2, HEIGHT - 24), pg.Color("white"), 'c', ALKHEM)

