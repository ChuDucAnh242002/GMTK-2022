import pygame
import os
import math
from pygame.locals import *
import engine.database as db
from engine.animation import animation

class object(animation):
    def __init__(self, ID, pos, status = "idle"):
        super().__init__(ID, pos, status)
        self.attack = 0
        self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.time = 0
        self.w_x = 0
        self.w_y = 0
        self.DDDH = [0, 0]
        self.hit_rect = 0
        self.movement = [0, 0]
        self.y_momentum = 0
        self.check = 0

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
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, movement) -> None:
        self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect = self.get_rect()

        # Update location x ---------------------------------------------------------------------------------------------------- #
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