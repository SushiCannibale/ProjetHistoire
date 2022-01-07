import pygame as pg

class AnimateSprite(pg.sprite.Sprite):
    def __init__(self, namesheet):
        super().__init__()
        self.spritesheet = pg.image.load(f'src/assets/spritesheets/{namesheet}.png')
        self.anim_index = 0
        self.last_anim = 0
        self.images = {
            'down': self.get_images(0),
            'right': self.get_images(18),
            'left': self.get_images(36),
            'up': self.get_images(54),
        }

        self.base_speed = 1
        self.speed = 1

    def get_image(self, x, y):
        image = pg.Surface((16, 17))
        image.blit(self.spritesheet, (0, 0), (x, y, 16, 17))
        return image

    def get_images(self, y):
        images = []
        for i in range(0, 4):
            x = i*16
            images.append(self.get_image(x, y))
        return images


    def change_anim(self, key):
        self.image = self.images[key][self.anim_index]
        self.image.set_colorkey((0, 255, 0))
        self.last_anim += self.speed * 8

        if self.last_anim >= 100:
            self.anim_index += 1
            if self.anim_index >= len(self.images[key]):
                self.anim_index = 0
            self.last_anim = 0