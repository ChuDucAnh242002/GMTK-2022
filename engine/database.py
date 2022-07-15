from numpy import multiply
import pygame
import os

FPS = 60
img_FPS = 12
delta_time = 0
multiply_factor = 0

img_database = {}

# { 'ID': [loc _img *60], ..... } . ID is filename  + status. ec=x: ID: coin_idle
animation_database = {}

# { 'ID': loc _img, ..... } . ID is filename + status. ec=x: ID: coin_idle
obj_database = {}

tile_rects = []
entities = []
objects = []

class database():
    global img_database, animation_database, obj_database
    global tile_rects, entities, objects

    def __init__(self, input_FPS, input_img_FPS):
        global FPS, img_FPS

        # { ID: [img_loaded, img_name, type] } type can be obj, tile, entity
        img_FPS = input_img_FPS
        FPS = input_FPS//img_FPS * img_FPS
        
        self.create_img_database()

        self.animation_path = 'data/animation'


        # { 'ID': [loc _img *60], ..... } . ID is filename + status. ec=x: ID: coin_idle
        self.create_animation_database(self.animation_path)

        self.obj_path = 'data/object'
        self.create_obj_database()

    def create_img_database(self):
        tile_path = 'data/tiles'
        object_path = 'data/object'
        entity_path = 'data/entity'
        ID = 1
        for tiles in os.listdir(tile_path):
            img = pygame.image.load(tile_path + '/' + tiles)
            img.set_colorkey([0, 0, 0])
            img_database[ID] = [img, tiles[:-4], 'tile']
            ID += 1
        for obj in os.listdir(object_path):
            img = pygame.image.load(object_path + '/' + obj)
            img.set_colorkey([0, 0, 0])
            img_database[ID] = [img, obj[:-4], 'object']
            ID += 1
        for entity in os.listdir(entity_path):
            img = pygame.image.load(entity_path + '/' + entity)
            img.set_colorkey([0, 0, 0])
            img_database[ID] = [img, entity[:-4], 'entity']
            ID += 1

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
