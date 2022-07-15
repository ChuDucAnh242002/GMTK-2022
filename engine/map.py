import pygame
import json
# from engine.database import database as db
from engine.entity import entity
from engine.object import object

import engine.database as db

class map():
    def __init__(self):

        # ID: [img_loaded, img_name, type] type can be obj, tile, entity
        self.game_map = {'tile': {}, # {'0;0': [[[pos_x, pos_y], ID] * n]}
                        'object': [], # [[[pos_x, pos_y], ID, name] * n]
                        'entity': [] # [[[pos_x, pos_y], ID, name] * n]
                        }
        self.player = None

    def load_map(self, name):

        # Only collide with camera
        db.tile_rects = []
        db.tile_ID = []
        db.object_camera = []
        db.entity_camera = []

        # All entities, obj in the game
        db.entities = []
        db.objects = []

        f = open('data/map/' + name + '.json', 'r')
        self.game_map = json.load(f)
        return self.game_map

    def update(self, camera):

        db.tile_rects = []  # Must clear else lag :<
        db.tile_ID = []

        for type in self.game_map:

            if type == 'tile':
                for chunk in self.game_map[type]:
                    for data in self.game_map[type][chunk]:
                        LOC_CHUNK = str(data[0][0]) + ';' + str(data[0][1])
                        pos_x = data[0][0]
                        pos_y = data[0][1]
                        ID_im = data[1]
                        data_width = db.img_database[ID_im][0].get_width()
                        data_height = db.img_database[ID_im][0].get_height()
                        block_rect = pygame.Rect(pos_x, pos_y, data_width, data_height)
                        if block_rect.colliderect(camera.rect):
                            if ID_im not in [1, 2, 3, 23, 37, 50, 55, 56, 57, 58]:
                                db.tile_rects.append(block_rect)
                                db.tile_ID.append(ID_im)

            elif type == 'entity' and db.entities == []:
                for data in self.game_map[type]:
                    temp_entity = entity(data[2], data[0])
                    if data[1] == 90:
                        if self.player == None:
                            self.player = temp_entity
                    else:
                        db.entities.append(temp_entity)

            elif type == 'object' and db.objects == []:
                for data in self.game_map[type]:
                    temp_object = object(data[2], data[0])
                    if data[1] == 79:
                        temp_object.change_status('closed')
                        strange_door_rect = temp_object.rect
                        strange_door_ex = True
                    elif data[1] == 78:
                        temp_object.change_tag(['tile', 'movable'])
                    
                    db.objects.append(temp_object)

        return self.player

    def render(self, surface, camera):
        scroll = camera.scroll

        for i in range(len(db.tile_ID)):
            img = db.img_database[db.tile_ID[i]][0]
            block_rect = db.tile_rects[i]
            surface.blit(img, [block_rect.x - scroll[0], block_rect.y - scroll[1]])

            # pygame.draw.rect(surface, [255, 0, 0],
            #                  [block_rect.x - scroll[0], block_rect.y - scroll[1], block_rect.width, block_rect.height], 1)
