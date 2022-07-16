import pygame
import os
from engine.core_funcs import *

FPS = 60
IMG_SIZE = 8
CHUNK_SIZE = 8
DEBUG = []

img_FPS = 12
delta_time = 0
multiply_factor = 0


# { 'type': [ [ID, surface] * n ]} . Ex: 'tile' : [ [0, bla bla], ...  ]
tiles_and_fore_database = {}

# { 'ID': [loc _img *60], ..... } . ID is filename  + status. ec=x: ID: coin_idle
animation_database = {}

# { 'ID': loc _img, ..... } . ID is filename + status. ec=x: ID: coin_idle
obj_database = {}

# Only collide with camera
tile_rects = []
tile_ID = []

fore_rects = []
fore_ID = []

object_camera = []
entity_camera = []

# All entities, obj in the game
entities = []
objects = []

# Collide table
COLLIDE_TABLE = [
    ['pass', 'none', '3', 'none'],
    ['none', 'pass', 'none', 'none'],
    ['float', 'none', 'blow', 'pass'],
    ['sink', '7', 'heavy', 'none']
]


class database():
    global img_database, animation_database, obj_database
    global tile_rects, entities, objects

    def __init__(self, input_FPS, input_img_FPS):
        global FPS, img_FPS

        # { ID: [img_loaded, img_name, type] } type can be obj, tile, entity
        img_FPS = input_img_FPS
        FPS = input_FPS//img_FPS * img_FPS
        
        self.tiles_path = 'data/tiles'
        self.tile_size = [IMG_SIZE, IMG_SIZE]
        self.create_tiles_and_fore_database()

        self.animation_path = 'data/animation'
        # { 'ID': [loc _img *60], ..... } . ID is filename + status. ec=x: ID: coin_idle
        self.create_animation_database(self.animation_path)

        self.obj_path = 'data/object'
        self.create_obj_database()

    def load_spritesheet_1(self, spritesheet, tile_size):
        """
        Param: full tileset image
        return: dict with num of each tile
        """
        rows = []
        spritesheet_dat = {}
        for y in range(spritesheet.get_height()):
            c = spritesheet.get_at((0, y))
            c = (c[0], c[1], c[2])
            if c == YELLOW:
                rows.append(y)

        num = 0 
        for row in rows:
            # row_content = []
            for x in range(spritesheet.get_width()):
                c = spritesheet.get_at((x, row))
                c = (c[0], c[1], c[2])
                if c == PINK:
                    img = clip(spritesheet, x, row + 1, tile_size[0], tile_size[1])
                    img.set_colorkey(COLORKEY)
                    # row_content.append(img)
                    spritesheet_dat[num] = img
                    num += 1
            # image for each row
            # spritesheet_dat.append(row_content)
        return spritesheet_dat

    def create_tiles_and_fore_database(self):
        # list of img name in path
        spritesheet_list = os.listdir(self.tiles_path)

        for img_file in spritesheet_list:
            # find png
            file_type = img_file.split('.')[-1]
            if file_type == 'png':
                file_path = self.tiles_path + '/' + img_file
                # Example: tiles
                file_name = img_file.split('.')[0]
                spritesheet_dat = self.load_spritesheet_1(pygame.image.load(file_path), self.tile_size)
                tiles_and_fore_database[file_name] = spritesheet_dat

    def create_animation_database(self, animation_path, animation_dir = []):

        if animation_dir == []:
            animation_dir = os.listdir(animation_path)

        for entity in animation_dir:
            entity_animation = os.listdir(animation_path + '/' + entity)
            if entity_animation[0][- 4:] == '.png':
                animation_database[entity] = []
                for frame in entity_animation:
                    for _ in range(int(FPS//img_FPS)):
                        animation_database[entity].append(animation_path + '/' + entity + '/' + frame)
            else:
                self.create_animation_database(animation_path + '/' + entity, entity_animation)

    def create_obj_database(self):
        obj_list = os.listdir(self.obj_path)
        for obj in obj_list:
            obj_database[obj[:len(obj) - 4]] = self.obj_path + '/' + obj
