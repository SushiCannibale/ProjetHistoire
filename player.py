import pygame as pg
from animator import AnimateSprite

class Character(AnimateSprite):
    def __init__(self, namesheet, pos):
        super().__init__(namesheet)
        self.pos = pos

        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 255, 0))
        self.rect = self.image.get_rect()

        self.feet = pg.Rect(0, 0, self.rect.width // 2, 12)
        self.last_pos = self.pos.copy() # duplication and not assignation

    def save_loc(self):
        self.last_pos = self.pos.copy()

    def move_back(self):
        self.pos = self.last_pos

    def move_right(self):
        self.change_anim('right')
        self.pos[0] += self.speed

    def move_left(self):
        self.change_anim('left')
        self.pos[0] -= self.speed

    def move_up(self):
        self.change_anim('up')
        self.pos[1] -= self.speed

    def move_down(self):
        self.change_anim('down')
        self.pos[1] += self.speed

    def update(self):
        self.rect.topleft = self.pos
        self.feet.midbottom = self.rect.midbottom

class Player(Character):
    def __init__(self):
        super().__init__("playerSP__16x17", [0, 0])
        self.collChest = False

class NPC(Character):
    def __init__(self, name, nb_points):
        super().__init__(name, [0, 0])
        self.nb_points = nb_points
        self.name = name

        self.points = [] # list of path points
        self.current_point = 0 # index of the list

        self.base_speed = 0.5
        self.speed = 0.5

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1
        if target_point >= self.nb_points:
            target_point = 0


        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def load_points(self, tmx_data):
        for n in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path_{n}")
            rect = pg.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

    def teleport_spawn(self):
        loc = self.points[self.current_point]
        self.pos[0] = loc.x
        self.pos[1] = loc.y
        self.save_loc()

