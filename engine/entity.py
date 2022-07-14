import pygame
import os
import math
from pygame.locals import *
from engine.database import database as db
from engine.object import object

class entity(object):
    def __init__(self, ID, pos, status = 'idle'):
        super().__init__(ID, pos, status)
        self.attack_timer = 0
        self.health = 100
        self.life = 1
        self.hitbox = self.rect

    def visible_area(self, width, height, double_height=False):
        vis_x = self.x - width * self.rect.width
        vis_y = self.y - self.rect.height * height
        vis_width = width * self.rect.width * 2 + self.rect.width
        if double_height:
            vis_height = self.rect.height * height * 2 + self.rect.height
        else:
            vis_height = self.rect.height * height + self.rect.height
        area_rect = pygame.Rect([vis_x, vis_y, vis_width, vis_height])
        return area_rect

    def one_time(self, status, offset=[0, 0]):
        ID = self.ID + '_' + status
        self.offset = offset
        self.change_action(status)
        if self.frame >= len(db.animation_database[ID]) - 1:
            self.offset = [0, 0]
            self.status = 'idle'
            self.frame = 0
            return True

    def attack_rect(self, area, offset):
        self.area = area
        self.attack = True
        if self.flip:
            if not self.one_time('sword_attack', offset):
                attack_rect = pygame.Rect(self.x - area, self.y, self.img.get_width(), self.img.get_height())
                return attack_rect
            else:
                self.attack = False
        else:
            if not self.one_time('sword_attack'):
                attack_rect = pygame.Rect(self.x + area, self.y, self.img.get_width(), self.img.get_height())
                return attack_rect
            else:
                self.attack = False

    def check_fall(self):
        fall = True
        if not self.flip:
            check_x = self.rect.x + self.rect.width
            check_y = self.rect.y + self.rect.height
        else:
            check_x = self.rect.x - self.rect.width
            check_y = self.rect.y + self.rect.height

        check_rect = pygame.Rect(check_x, check_y, self.rect.width, self.rect.height)
        for tile_check in db.tile_rects:
            if check_rect.colliderect(tile_check):
                fall = False
        if fall:
            return True