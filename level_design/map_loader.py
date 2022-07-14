import pygame, os, sys

from core_funcs import *

TOTAL_LEVEL = 0
game_map = {'tile': {}, 
            'object': [],
            'entity': []
            }

ALL_LAYER = []
TILE_LAYER = ["tile_layer_0"]
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
            'object': [],
            'entity': []
            }
        entities = load_entity(level, json_map)
        tiles = load_tile(level, json_map)
        game_map[level]["entity"] = entities
        game_map[level]["tile"] = tiles
    print(game_map)

def load_tile(level, json_map):
    tiles = {}
    data2D = json_map[level]["tile_layer_0"]
    for y in range(len(data2D)):
        for x in range(len(data2D[0])):
            loc = [x *IMG_SIZE, y *IMG_SIZE]
            pos_chunk = str(int(x // CHUNK_SIZE)) + ';' + str(int(y // CHUNK_SIZE))
            id = data2D[y][x]
            data = [loc, id]
            if pos_chunk not in tiles:
                tiles[pos_chunk] = [data]
            elif data not in tiles[pos_chunk]:
                tiles[pos_chunk].append(data)
    return tiles

def load_entity(level, json_map):
    entities = []
    for entity in json_map[level]["entity_layer_0"]:
        x = entity['x'] - entity['originX']
        y = entity['y'] - entity['originY']
        id = entity['name']
        entities.append([[x, y], id])
    return entities
    

load_map("data/map/")