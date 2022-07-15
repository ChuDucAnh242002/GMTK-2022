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
        f = open('data/map/' + name + '.json', 'r')
        self.game_map = json.load(f)
        return self.game_map

    def update(self, display_rect):

        db.tile_rects = []  # Must clear else lag :<
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
                        if block_rect.colliderect(display_rect):
                            if ID_im not in [1, 2, 3, 23, 37, 50, 55, 56, 57, 58]:
                                db.tile_rects.append(block_rect)

            elif type == 'entity' and db.entities == []:
                for data in self.game_map[type]:
                    temp_entity = entity(data[2], data[0])
                    if data[1] == 90:
                        self.player = temp_entity
                    elif temp_entity.rect.colliderect(display_rect):
                        db.entities.append(temp_entity)

            elif type == 'object' and db.objects == []:
                for data in self.game_map[type]:
                    if data[1] == 79:
                        db.objects.append(object(data[2], data[0], 'closed'))
                        strange_door_rect = db.objects[-1].get_rect()
                        strange_door_ex = True
                    elif data[1] == 62:
                        db.objects.append(object(data[2], data[0]))
                    elif data[1] == 64:
                        db.objects.append(object(data[2], data[0]))  # ID, pos
                    elif data[1] == 78:
                        db.tile_rects.append(object(data[2], data[0]).get_rect())
                    else:
                        db.objects.append(object(data[2], data[0]))
        return self.player

    def render(self, surface, camera):
        scroll = camera.scroll

        for chunk in self.game_map['tile']:
            for data in self.game_map['tile'][chunk]:
                LOC_CHUNK = str(data[0][0]) + ';' + str(data[0][1])
                pos_x = data[0][0]
                pos_y = data[0][1]
                ID_im = data[1]
                img = db.img_database[ID_im][0]
                data_width = db.img_database[ID_im][0].get_width()
                data_height = db.img_database[ID_im][0].get_height()
                block_rect = pygame.Rect(pos_x, pos_y, data_width, data_height)
                if block_rect.colliderect(camera.rect):
                    surface.blit(img, [pos_x - scroll[0], pos_y - scroll[1]])
                    # pygame.draw.rect(surface, [255, 0, 0],
                    #                  [pos_x - scroll[0], pos_y - scroll[1], data_width, data_height], 1)
