from dataclasses import dataclass
import pygame as pg
import pyscroll as ps
import pytmx

from player import *


@dataclass
class Portal:
    from_world: str
    origin_point: str
    to_world: str
    tp_point: str

@dataclass
class Map:
    name: str
    walls: [pg.Rect]
    chests: [pg.Rect]
    group: ps.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: [Portal]
    npcs: [NPC]

class MapManager:
    def __init__(self, game, screen, player):
        self.game = game
        self.screen = screen
        self.player = player
        self.maps = {} # 'name' -> Map('house', walls, groups)
        self.current_map = "house1"

        self.register_map("house1", npcs=[NPC("naziSP__16x17", nb_points=4), NPC("nazi2", nb_points=2)])

        self.teleport_player('spawn_h1')
        self.teleport_npcs()

    def register_map(self, name, portals=[], npcs=[]):
        tmx_data = pytmx.util_pygame.load_pygame(f'src/assets/maps/{name}.tmx')
        map_data = ps.data.TiledMapData(tmx_data)
        map_layer = ps.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # colliders list
        walls = []
        chests = []
        for obj in tmx_data.objects:
            if obj.type == 'wall':
                walls.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == 'chest':
                chests.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))

        group = ps.PyscrollGroup(map_layer, default_layer=3)
        group.add(self.player) # draw player
        for npc in npcs: # draw npcs
            group.add(npc)

        # create map object
        self.maps[name] = Map(name, walls, chests, group, tmx_data, portals, npcs)

    def get_current_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_current_map().group

    def get_walls(self):
        return self.get_current_map().walls

    def get_chests(self):
        return self.get_current_map().chests

    def get_obj(self, name):
        return self.get_current_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def check_collisions(self):
        # portals
        for portal in self.get_current_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_obj(portal.origin_point)
                rect = pg.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.to_world
                    self.teleport_player(copy_portal.tp_point)

        # walls
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                    self.game.end_game_over()
                else:
                    sprite.speed = sprite.base_speed
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

            if type(sprite) is not NPC:
                if sprite.feet.collidelist(self.get_chests()) > -1:
                    self.player.collChest = True
                    self.game.collectibles[self.game.collectible_key][0] = True
                elif self.player.collChest:
                    if self.game.collectible_key == "paper":
                        self.game.collectible_key = "radio"
                    elif self.game.collectible_key == "radio":
                        self.game.collectible_key = "dollar"
                    self.player.collChest = False

    def teleport_player(self, name):
        point = self.get_obj(name)
        self.player.pos[0] = point.x
        self.player.pos[1] = point.y
        self.player.save_loc() # case player got tp on collider

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_current_map().npcs:
            npc.move()

