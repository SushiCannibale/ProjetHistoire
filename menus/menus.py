import pygame as pg

class Menu:
    def __init__(self, game):
        self.game = game

        self.doDisplay = False

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

    def display(self):
        self.doDisplay = True
        while self.doDisplay:
            self.game.refreshDisplay()
            self.game.events()
            pg.draw.rect(self.game.screen, pg.Color("red"), [10, 10, 100, 200])
            pg.display.flip()

