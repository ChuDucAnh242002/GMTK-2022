import pygame, os, sys

from core_funcs import *

TOTAL_LEVEL = 0
game_map = {'tile': {}, 
            'object': [],
            'entity': []
            }

ALL_LAYER = []
TILE_LAYER = ["tile_layer_0", "tile_layer_1"]
ENTITY_LAYER = ["entity_layer_0"]
ALL_LAYER.extend(TILE_LAYER)
ALL_LAYER.extend(ENTITY_LAYER)
IMG_SIZE = 8
CHUNK_SIZE = 8

def load_map(domain):
    game_map = {}
    json_map = load_dict_json(domain, TOTAL_LEVEL, ALL_LAYER)
    for level in range(TOTAL_LEVEL +1):
        game_map[level] = {'tile': {}, 
            'foreground': [],
            'object': [],
            'entity': []
            }
        entities = load_entity(level, json_map)
        tiles, foreground = load_tile(level, json_map)
        game_map[level]["entity"] = entities
        game_map[level]["tile"] = tiles
        game_map[level]["foreground"] = foreground

    return game_map

def load_tile(level, json_map):
    tiles = {}
    foreground = {}
    data2D_tile = json_map[level]["tile_layer_0"]
    data2D_fore = json_map[level]["tile_layer_1"]
    for y in range(len(data2D_tile)):
        for x in range(len(data2D_tile[0])):
            loc = [x *IMG_SIZE, y *IMG_SIZE]
            pos_chunk = str(int(x // CHUNK_SIZE)) + ';' + str(int(y // CHUNK_SIZE))
            id_tile = data2D_tile[y][x]
            id_fore = data2D_fore[y][x]
            data_tile = [loc, id_tile]
            data_fore = [loc, id_fore]
            if pos_chunk not in tiles:
                tiles[pos_chunk] = [data_tile]
            elif data_tile not in tiles[pos_chunk]:
                tiles[pos_chunk].append(data_tile)

            if pos_chunk not in foreground:
                foreground[pos_chunk] = [data_fore]
            elif data_fore not in foreground[pos_chunk]:
                foreground[pos_chunk].append(data_fore)
    return tiles, foreground

def load_entity(level, json_map):
    entities = []
    for entity in json_map[level]["entity_layer_0"]:
        x = entity['x'] - entity['originX']
        y = entity['y'] - entity['originY']
        id = entity['name']
        entities.append([[x, y], id])
    return entities
    
# game_map = load_map("data/map/")
# print(game_map)