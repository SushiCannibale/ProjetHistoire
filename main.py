import pygame as pg
import pytmx
import pyscroll

from player import *
from map import MapManager

FPS = 60
UP, DOWN, LEFT, RIGHT, INTERACT = 122, 115, 113, 100, 101
WIDTH, HEIGHT = 1080, 720

ALKHEM = 'src/assets/fonts/Alkhemikal.ttf'

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Résistance - Jeu 1")
        self.overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.overlay.fill(pg.Color("#121212"))
        self.overlay.set_alpha(50)

        self.isRunning, self.isPlaying = True, False
        self.hasWin = False

        self.collectibles = {
            "paper": [False, pg.transform.scale(pg.image.load('src/assets/spritesheets/paper.png'), (64, 64)), [270 - 32, 10]],
            "radio": [False, pg.transform.scale(pg.image.load('src/assets/spritesheets/radio.png'), (64, 64)), [540 - 32, 10]],
            "dollar": [False, pg.transform.scale(pg.image.load('src/assets/spritesheets/dollar.png'), (152, 76)), [810 - 76, 10]]
        }
        self.collectible_key = "paper"


        # player
        self.player = Player()
        self.map_manager = MapManager(self, self.screen, self.player)

        self.clock = pg.time.Clock()

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.isRunning = False
                pg.quit()

            if e.type == pg.KEYDOWN:
                if e.key == ord('e'):
                    self.isPlaying = True

    def inputs(self):
        pressed = pg.key.get_pressed()

        if pressed[LEFT]:
            self.player.move_left()
        if pressed[RIGHT]:
            self.player.move_right()
        if pressed[UP]:
            self.player.move_up()
        if pressed[DOWN]:
            self.player.move_down()

    def update(self):
        self.map_manager.update()

    def loop(self):
        while self.isRunning:
            self.player.save_loc()

            self.events()
            self.inputs()
            self.map_manager.draw()
            self.update()

            self.screen.blit(self.overlay, (0, 0))
            pg.draw.rect(self.screen, pg.Color("#121212"), [0, 0, WIDTH, 100])

            self.blit_collectibles()

            if self.collectibles["paper"][0] is True and self.collectibles["radio"][0] is True and self.collectibles["dollar"][0] is True:
                self.end_game_win()
                break

            pg.display.flip()
            self.clock.tick(FPS)

    def blit_collectibles(self):
        for key in self.collectibles.keys():
            if self.collectibles[key][0]:
                self.screen.blit(self.collectibles[key][1], self.collectibles[key][2])

    def start_menu(self):
        while not self.isPlaying:
            self.events()
            self.screen.fill(pg.Color("#121212"))
            self.draw_text("Votre mission", 64, WIDTH//2, 64, pg.Color("green"), 'c', ALKHEM)
            self.draw_text("Vous devez récupérer le plus", 32, WIDTH//2, HEIGHT//2 - 32, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("de ressources pour la résistance.", 32, WIDTH//2, HEIGHT//2, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("Vous devrez trouver", 32, WIDTH//2, HEIGHT//2 + 32, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("Une pile de papier, une radio, et de l'argent", 32, WIDTH//2, HEIGHT//2 + 64, pg.Color("green"), 'c', ALKHEM)
            self.draw_text("cachés dans des coffres en bois", 32, WIDTH//2, HEIGHT//2 + 96, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("Sans vous faire repérer par l'ennemi !", 32, WIDTH//2, HEIGHT//2 + 128, pg.Color("red"), 'c', ALKHEM)
            self.draw_text("...Appuyez sur 'e' pour commencer...", 32, WIDTH//2, HEIGHT - 32, pg.Color("gray50"), 'c', ALKHEM)

            pg.display.update()
            self.clock.tick(60)

    def end_game_win(self):
        while True:
            self.events()
            self.screen.fill(pg.Color("#121212"))
            self.draw_text("Mission réussie !", 64, WIDTH//2, 64, pg.Color("green"), 'c', ALKHEM)
            self.draw_text("Bravo, vous avez réussi à récupérer", 48, WIDTH//2, HEIGHT//2, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("les ressources dont la résistance", 48, WIDTH//2, HEIGHT//2 + 48, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("avait besoin !", 48, WIDTH//2, HEIGHT//2 + 96, pg.Color("white"), 'c', ALKHEM)

            pg.display.update()
            self.clock.tick(60)

    def end_game_over(self):
        while True:
            self.events()
            self.screen.fill(pg.Color("#121212"))
            self.draw_text("Vous vous êtes fait repéré !", 64, WIDTH//2, 64, pg.Color("red"), 'c', ALKHEM)
            self.draw_text("Les soldats de la Wehrmacht vous ont repérés !", 32, WIDTH//2, HEIGHT//2, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("Vous connaissiez les dangers de l'engagement dans la résistance...", 32, WIDTH//2, HEIGHT//2 + 64, pg.Color("white"), 'c', ALKHEM)
            self.draw_text("Votre aventure s'arrête ici...", 32, WIDTH//2, HEIGHT//2 + 96, pg.Color("white"), 'c', ALKHEM)

            pg.display.update()
            self.clock.tick(60)

    def draw_text(self, text, size, x, y, color, align, fontname):
        """
        Draws text on a surface
        """
        font = pg.font.Font(fontname, size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if align in ['up', 'u']:
            text_rect.midtop = (x, y)
        if align in ['down', 'd']:
            text_rect.midbottom = (x, y)
        if align in ['left', 'l']:
            text_rect.midleft = (x, y)
        if align in ['right', 'r']:
            text_rect.midright = (x, y)

        if align in ['upleft', 'ul']:
            text_rect.topleft = (x, y)
        if align in ['upright', 'ur']:
            text_rect.topright = (x, y)
        if align in ['downleft', 'dl']:
            text_rect.bottomleft = (x, y)
        if align in ['downright', 'dr']:
            text_rect.bottomright = (x, y)

        if align in ['center', 'c']:
            text_rect.center = (x, y)

        self.screen.blit(text_surf, text_rect)



if __name__ == "__main__":
    game = Game()
    game.start_menu()
    game.loop()
