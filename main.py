import pygame as pg
import os
import socket
import json
import threading
import time
import dill


class Client:
    def __init__(self, conn, addr, user_id: str):
        self.player = None
        for entity in game.inactive_entities:
            if type(entity) == Player and entity.player_id == user_id:
                self.player = entity
        if self.player is None:
            self.player = Player((0, 0), user_id)
            game.entities.append(self.player)
        self.conn = addr
        self.addr = addr

    def on_disconnect(self):
        game.entities.remove(self.player)
        game.inactive_entities.append(self.player)

    def send(self):
        pass
        # this is how you can send stuff

    def handle(self):
        pass
        # basically this is where you can code the handleing stuff


class Entity(pg.sprite.Sprite):
    def __init__(self, location: tuple, entity_id: str):
        super(Entity, self).__init__()
        self.location = location
        self.id = entity_id
        self.data = Game.get_data(self.id)

        self.image = []
        self.images = []
        if type(self.data['image']) == list:
            for image in self.data['image']:
                self.images.append(pg.image.load(image).convert_alpha())
        else:
            self.images = [pg.image.load(self.data['image']).convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.location

        self.health = self.data['health']
        self.attack_damage = self.data['attack_damage']
        self.speed = self.data['speed']
        self.attack_speed = self.data['attack_speed']

        self.inventory = {}

    def path_find(self, destination: tuple):
        pass
        # code a star for pathfinding

    def tick(self, frame: int, initial_time: float):
        try:
            with open(self.data['tick']) as tick_file:
                exec(tick_file.read())
        except KeyError:
            self.default_tick(frame, initial_time)

    def default_tick(self, frame: int, initial_time: float):
        if frame % 15 == 0:
            try:
                self.image = self.images[self.images.index(self.image)+1]
            except IndexError:
                self.image = self.image[0]
        # default tick function

    def action(self):
        pass


class Player(Entity):
    def __init__(self, location: tuple, player_id: str):
        super(Player, self).__init__(location, 'entities:player')
        self.player_id = player_id

    def input(self, key):
        pass
        # so basically just perform some sort of action here idk


class SelectionBox(pg.sprite.Sprite):
    def __init__(self, location: tuple, size: int):
        super(SelectionBox, self).__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(pg.Color(0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = location


class Item:
    def __init__(self, item_id):
        self.id = item_id
        self.data = Game.get_data(item_id)
        self.image = pg.image.load(self.data['image']).convert_alpha()

    def draw(self, surface: pg.Surface, location: tuple):
        surface.blit(self.image, location)


class Tile(pg.sprite.Sprite):
    def __init__(self, location: tuple, tile_id: str):
        super(Tile, self).__init__()
        self.location = location
        self.id = tile_id
        self.data = Game.get_data(self.id)

        self.image = []
        self.images = []
        if type(self.data['image']) == list:
            for image in self.data['image']:
                self.images.append(pg.image.load(image).convert_alpha())
        else:
            self.images = [pg.image.load(self.data['image']).convert_alpha()]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.location

    def interact(self, target: Entity):
        try:
            with open(self.data['tick']) as interact_file:
                exec(interact_file.read())
        except KeyError:
            pass

    def alternate_interact(self, target: Entity):
        try:
            with open(self.data['tick']) as alternate_interact_file:
                exec(alternate_interact_file.read())
        except KeyError:
            pass

    def tick(self, frame: int, initial_time: float):
        try:
            with open(self.data['tick']) as tick_file:
                exec(tick_file.read())
        except KeyError:
            self.default_tick(frame, initial_time)

    def default_tick(self, frame: int, initial_time: float):
        if frame % 15 == 0:
            try:
                self.image = self.images[self.images.index(self.image) + 1]
            except IndexError:
                self.image = self.image[0]
        # default tick function


class Game:
    def __init__(self):
        # ok so basically for now just make the base game
        # this will be where all of the variables will be initialized
        self.running = True
        self.window_size = (1280, 720)
        self.scale = 64

        self.current_level = "test"
        # these variables will be from the level data

        with open(f"data/levels{self.current_level}/level.pickle", "rb") as level_file:
            self.level = dill.load(level_file)

        with open(f"data/levels{self.current_level}/entities.pickle", "rb") as entity_file:
            self.entities = dill.load(entity_file)

        with open(f"data/levels{self.current_level}/inactive_entities.pickle", "rb") as inactive_entities_file:
            self.inactive_entities = dill.load(inactive_entities_file)

        self.initial_time = time.time()

        # inactive_entities are stored here and can be reactivated later

        # so essentially I need the local player this way I can control the local player
        # the way that the server is going to work is that all of the clients are going to send their movements to
        # the server, and the server is actually going to process everything, this is the server, the clients will
        # just be displays that catch keystrokes
        self.display = pg.Surface(self.window_size)
        # send this surface to the clients and they will display them on their screens

    def run(self):
        # this will be where the actual game is coded
        pass

    def get_scale(self):
        return self.scale

    def stop(self):
        self.running = False
        with open(f"data/levels{self.current_level}/level.pickle", "wb") as level_file:
            dill.dump(self.level, level_file)

        with open(f"data/levels{self.current_level}/entities.pickle", "wb") as entity_file:
            dill.dump(self.entities, entity_file)

        with open(f"data/levels{self.current_level}/inactive_entities.pickle", "wb") as inactive_entities_file:
            dill.dump(self.inactive_entities, inactive_entities_file)

    def get_data(self, data_id: str):
        with open(f"data/{data_id.replace(':', '/')}") as data_file:
            return json.load(data_file)

    def draw(self, surface: pg.Surface, *groups):
        for group in groups:
            try:
                for item in group:
                    item.draw(surface)
            except TypeError:
                group.draw(surface)

    def tick(self, frame, initial_time, *groups):
        for group in groups:
            try:
                for item in group:
                    item.tick(frame, initial_time)
            except TypeError:
                group.tick(frame, initial_time)


if __name__ == '__main__':
    game = Game()
    game.run()
    game.stop()
