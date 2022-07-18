from math import gamma
from socket import gethostbyname_ex
from numpy import tile
import pygame
import json
# from engine.database import database as db
from engine.entity import entity
from engine.object import object

import engine.database as db
from engine.core_funcs import *

from mechanic.player import player

class map():
    def __init__(self):

        # ID: [img_loaded, img_name, type] type can be obj, tile, entity
        self.game_map = {
            'tile': {}, # {'0;0': [[[pos_x, pos_y], ID] * n]}
            'foreground': {}, # {'0;0': [[[pos_x, pos_y], ID] * n]}
            'object': [], # [[[pos_x, pos_y], ID] * n]
            'entity': [] # [[[pos_x, pos_y], ID] * n]
            }

        self.player = None

        self.domain = 'data/map/'
        self.ALL_LAYER = []
        self.TILE_LAYER = ["tile_layer_0", "tile_layer_1"]
        self.ENTITY_LAYER = ["entity_layer_0", "entity_layer_1"]
        self.ALL_LAYER.extend(self.TILE_LAYER)
        self.ALL_LAYER.extend(self.ENTITY_LAYER)

    def load_map(self, level):
        json_map = load_dict_json(self.domain, level, self.ALL_LAYER)

        self.game_map = {'tile': {}, 
            'foreground': [],
            'object': [],
            'entity': []
            }
        tiles, foreground = self.load_tile(json_map)
        entities, objects = self.load_entity(json_map)
        self.game_map["tile"] = tiles
        self.game_map["foreground"] = foreground
        self.game_map["entity"] = entities
        self.game_map["object"] = objects

    def load_tile(self, json_map):
        tiles = {}
        foreground = {}
        data2D_tile = json_map["tile_layer_0"]
        data2D_fore = json_map["tile_layer_1"]

        TILE_SIZE = data2D_tile[1]
        data2D_tile = data2D_tile[0]
        FORE_SIZE = data2D_fore[1]
        data2D_fore = data2D_fore[0]

        for y in range(len(data2D_tile)):
            for x in range(len(data2D_tile[0])):
                loc = [x * TILE_SIZE[0], y * TILE_SIZE[1]]
                pos_chunk = str(int(x // db.CHUNK_SIZE)) + ';' + str(int(y // db.CHUNK_SIZE))
                id_tile = data2D_tile[y][x]
                data_tile = [loc, id_tile]

                if id_tile != -1:
                    if pos_chunk not in tiles:
                        tiles[pos_chunk] = [data_tile]
                    elif data_tile not in tiles[pos_chunk]:
                        tiles[pos_chunk].append(data_tile)

        for y in range(len(data2D_fore)):
            for x in range(len(data2D_fore[0])):
                loc = [x * FORE_SIZE[0], y * FORE_SIZE[1]]
                pos_chunk = str(int(x // db.CHUNK_SIZE)) + ';' + str(int(y // db.CHUNK_SIZE))
                id_fore = data2D_fore[y][x]
                data_fore = [loc, id_fore]

                if id_fore != -1:
                    if pos_chunk not in foreground:
                        foreground[pos_chunk] = [data_fore]
                    elif data_fore not in foreground[pos_chunk]:
                        foreground[pos_chunk].append(data_fore)

        return tiles, foreground

    def load_entity(self, json_map):
        entities = []
        objects = []
        if "entity_layer_0" in self.ENTITY_LAYER:
            for entity in json_map["entity_layer_0"]:
                try:
                    x = entity['x'] + entity['originX']
                    y = entity['y'] + entity['originY']
                except:
                    x = entity['x']
                    y = entity['y']

                name = entity['name']
                # id = entity['id']

                # x, y = x * db.IMG_SIZE / 8, y * db.IMG_SIZE / 8


                entities.append([[x, y], name])
        if "entity_layer_1" in self.ENTITY_LAYER:
            for entity in json_map["entity_layer_1"]:
                try:
                    x = entity['x'] + entity['originX']
                    y = entity['y'] + entity['originY']
                except:
                    x = entity['x']
                    y = entity['y']

                name = entity['name']
                # id = entity['id']

                # x, y = x * db.IMG_SIZE / 8, y * db.IMG_SIZE / 8

                objects.append([[x, y], name])
        return entities, objects

    def update(self, camera):
        for type in self.game_map:

            if type == 'tile':
                for chunk in self.game_map[type]:
                    for data in self.game_map[type][chunk]:
                        LOC_CHUNK = str(data[0][0]) + ';' + str(data[0][1])
                        pos_x = data[0][0]
                        pos_y = data[0][1]
                        ID_im = data[1]
                        data_width = db.tiles_and_fore_database[type][ID_im].get_width()
                        data_height = db.tiles_and_fore_database[type][ID_im].get_height()
                        block_rect = pygame.Rect(pos_x, pos_y, data_width, data_height)
                        if block_rect.colliderect(camera.rect):
                            db.tile_rects.append(block_rect)
                            db.tile_ID.append(ID_im)
            elif type == 'foreground':
                for chunk in self.game_map[type]:
                    for data in self.game_map[type][chunk]:
                        LOC_CHUNK = str(data[0][0]) + ';' + str(data[0][1])
                        pos_x = data[0][0]
                        pos_y = data[0][1]
                        ID_im = data[1]
                        data_width = db.tiles_and_fore_database[type][ID_im].get_width()
                        data_height = db.tiles_and_fore_database[type][ID_im].get_height()
                        block_rect = pygame.Rect(pos_x, pos_y, data_width, data_height)
                        if block_rect.colliderect(camera.rect):
                            db.fore_rects.append(block_rect)
                            db.fore_ID.append(ID_im)
            elif type == 'entity' and db.entities == []:
                for data in self.game_map[type]:
                    if data[1] == 'player' or data[1] == 'Player':
                        if self.player == None:
                            self.player = player(data[1], data[0])
                            self.player.set_spawn(data[0])
                    else:
                        temp_entity = entity(data[1], data[0])
                        db.entities.append(temp_entity)

            elif type == 'object':
                if db.objects == []:
                    for data in self.game_map[type]:
                        temp_object = object(data[1], data[0])
                        db.objects.append(temp_object)
                else:
                    for data in self.game_map[type]:
                        temp_object = object(data[1], data[0])
                        if temp_object.ID == 'rock':
                            db.tile_rects.append(temp_object.rect)

        return self.player

    def render(self, surface, camera):
        scroll = camera.scroll

        bg = pygame.image.load('data/background/Background.png').convert()
        bg = pygame.transform.scale(bg, [camera.rect.width, camera.rect.height])
        surface.blit(bg, [camera.x - scroll[0], camera.y - scroll[1]])

        for i in range(len(db.tile_ID)):
            img = db.tiles_and_fore_database['tile'][db.tile_ID[i]]
            block_rect = db.tile_rects[i]
            
            if 'hide_tile' not in db.DEBUG:
               surface.blit(img, [block_rect.x - scroll[0], block_rect.y - scroll[1]])
        
        for i in range(len(db.fore_ID)):
            img = db.tiles_and_fore_database['foreground'][db.fore_ID[i]]
            block_rect = db.fore_rects[i]
            
            if 'hide_fore' not in db.DEBUG:
               surface.blit(img, [block_rect.x - scroll[0], block_rect.y - scroll[1]])
        
            # pygame.draw.rect(surface, [255, 0, 0],
            #                  [block_rect.x - scroll[0], block_rect.y - scroll[1], block_rect.width, block_rect.height], 1)
