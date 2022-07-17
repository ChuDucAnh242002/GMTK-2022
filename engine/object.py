from shutil import move
import pygame
import os
import math
from pygame.locals import *
import engine.database as db
from engine.animation import animation

class object(animation):
    def __init__(self, ID, pos, status = "idle", tag = ['object']):
        super().__init__(ID, pos, status, tag)
        self.attack = 0
        self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.near_by = {'left': [], 'right': [], 'up': [], 'down': [], 'surround': []}
        self.time = 0
        self.w_x = 0
        self.w_y = 0
        self.DDDH = [0, 0]
        self.hit_rect = 0
        self.movement = [0, 0]
        self.y_momentum = 0
        self.check = 0
        self.friction = [0, 0]
        self.spawn_pos = [0, 0]

    def set_spawn(self, pos):
        self.spawn_pos = pos.copy()

    def render(self, surface, camera, draw=True) -> None:
        super().render(surface, camera, draw)
        self.update()
    
    def update(self):
        super().update()
        self.update_tag()
        self.update_near_by()

    def update_tag(self):
        if 'tile' in self.tag:
            db.tile_rects.append(self.rect)
        if 'movable' in self.tag:
            pass
        if 'object' in self.tag:
            pass
        if 'entity' in self.tag:
            pass

    def update_near_by(self):
        self.near_by = {'left': [], 'right': [], 'up': [], 'down': [], 'surround': []}

        direction = ['left', 'right', 'up', 'down', 'surround']

        if 'entity' in self.tag or 'movable' in self.tag:
            for tile in db.tile_rects:
                for direc in direction:
                    if self.get_nearby_rect(direc).colliderect(tile):
                        self.near_by[direc].append('tile')
            
            for object in db.object_camera:
                for direc in direction:
                    if (self.get_nearby_rect(direc)).colliderect(object.rect):
                        self.near_by[direc].append(object)
            
            for entity in db.entity_camera:
                for direc in direction:
                    if (self.get_nearby_rect(direc)).colliderect(entity.rect):
                        self.near_by[direc].append(entity)

    def get_nearby_rect(self, way):
        multi_x = 0
        multi_y = 0
        offset = [16, 16]
        
        if (way == 'left'):
            multi_x = -1
        if (way == 'right'):
            multi_x = self.width / offset[0]
        if (way == 'up'):
            multi_y = -1
        if (way == 'down'):
            multi_y = self.height /offset[1]

        if way != 'surround':
            
            if (way == 'left' or way == 'right'):
                nearby_x = self.x + multi_x * offset[0]
                nearby_y = self.y + multi_y * self.height
                return pygame.Rect(nearby_x, nearby_y, offset[0], self.height)
            else:
                nearby_x = self.x + multi_x * self.width
                nearby_y = self.y + multi_y * offset[1]
                return pygame.Rect(nearby_x, nearby_y, self.width, offset[1])
            
            
        else:
            radius = [1, 1]

            nearby_x = self.x - radius[0]
            nearby_y = self.y - radius[1]
            return pygame.Rect(nearby_x, nearby_y, self.width + radius[0] * 2, self.height + radius[1] * 2)

    def DDDH(self, w, A, width, height, offset=[0, 0]) -> None:
        self.w_x = w[0]
        self.w_y = w[1]
        a_x = A[0]
        a_y = A[1]
        if self.time == 54:
            self.time = 0
        offset_x = a_x * math.cos(self.w_x * self.time + math.pi / 2)
        offset_y = a_y * math.cos(self.w_y * self.time)
        hit_box = pygame.Rect([self.x + offset_x + offset[0], self.y + offset_y + offset[1], width, height])
        self.time += 1

    def collide_test(self) -> list:
        hit_list = []
        for tile in db.tile_rects:
            if self.rect.colliderect(tile) and tile != self.rect:
                hit_list.append(tile)
        return hit_list

    def move(self, movement) -> None:

        movement = [round(movement[0] * db.multiply_factor), round(movement[1] * db.multiply_factor)]
        self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}

        # Update location x ---------------------------------------------------------------------------------------------------- #
        if movement[0] >= self.friction[0]:
            movement[0] -= self.friction[0]
        elif movement[0] < -self.friction[0]:
            movement[0] += self.friction[0]
        else:
            movement[0] = 0

        self.rect.x += movement[0]
        hit_list = self.collide_test()
        for tile in hit_list:
            if movement[0] > 0:
                self.collision['right'] = True
                self.rect.right = tile.left
            elif movement[0] < 0:
                self.collision['left'] = True
                self.rect.left = tile.right
        self.x = self.rect.x

        # Update location y ------------------------------------------------------------------------------------------------------------------ #
        if movement[1] <= -self.friction[1]:
            movement[1] += self.friction[1]
        elif movement[1] > self.friction[1]:
            movement[1] -= self.friction[1]
        else:
            movement[1] = 0
        
        self.rect.y += movement[1]
        hit_list = self.collide_test()
        for tile in hit_list:
            if movement[1] >= 0:
                self.collision['bottom'] = True
                self.rect.bottom = tile.top
            elif movement[1] < 0:
                self.collision['top'] = True
                self.rect.top = tile.bottom
        self.y = self.rect.y

        self.pos = [self.x, self.y]

    def attack_area(self, area, offset = [0, 0]) -> pygame.Rect:
        attack_x = self.x + offset[0] - area[0]
        attack_y = self.y + offset[1] - area[1]
        attack_width = area[0] * 2 + self.get_rect().width
        attack_height = area[1] * 2 + self.get_rect().height

        attack_area = pygame.Rect(attack_x, attack_y, attack_width, attack_height)
        return attack_area

    def change_action(self, status, offset=[0, 0]) -> None:
        self.offset = offset
        if self.status != status:
            self.status = status
            self.frame = 0

    def change_tag(self, tag):
        self.tag = tag

    def add_tag(self, tag):
        self.tag.append(tag)