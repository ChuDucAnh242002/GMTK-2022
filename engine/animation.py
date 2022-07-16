from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import pygame
import os
import engine.database as db

from engine.core_funcs import *

class animation():
    def __init__(self, ID, pos, status, tag):
        self.animation_path = 'data/animation'
        self.entity_path = "data/animation/entity"
        self.obj_path = "data/object"
        self.FPS = db.FPS
        self.img_FPS = db.img_FPS
        self.frame = 0
        self.ID = ID
        self.status = status
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.offset = [0, 0]
        if 'no_img' in db.DEBUG:
            self.rect = pygame.Rect(self.x, self.y, db.IMG_SIZE, db.IMG_SIZE)
        else:
            self.rect = self.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.flip = False
        self.tag = tag

    def render(self, surface, camera, draw = True) -> None:

        self.x = self.pos[0]
        self.y = self.pos[1]

        scroll = camera.scroll
        pos = [self.pos[0] - scroll[0] + self.offset[0], self.pos[1] - scroll[1] + self.offset[1]]

        if 'no_img' in db.DEBUG:
            BODER = 0
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.rect.width, self.rect.height)
            if 'player' in self.tag:
                COLOR = RED  
            else:

                if 'element' not in self.ID:
                    BODER = 1
                
                if 'water' in self.ID:
                    COLOR = BLUE
                elif 'fire' in self.ID:
                    COLOR = RED
                elif 'wind' in self.ID:
                    COLOR = GREEN
                elif 'rock' in self.ID:
                    COLOR = PINK
                elif 'light' in self.ID:
                    COLOR = WHITE
                elif 'dark' in self.ID:
                    COLOR = DARK_PURPLE
                elif self.ID == 'energy_ball':
                    COLOR = CYAN
                elif self.ID == 'gate':
                    COLOR = PURPLE
            
            pygame.draw.rect(surface, COLOR, [pos[0], pos[1], self.rect.width, self.rect.height], BODER)
        else:
            obj_list = os.listdir(self.obj_path)
            animation_list = os.listdir(self.animation_path)
            entity_list = os.listdir(self.animation_path + '/entity')

            if self.ID in animation_list or self.ID in entity_list:
                try:
                    check_list = os.listdir(self.animation_path + '/' + self.ID)
                except:
                    check_list = os.listdir(self.animation_path + '/entity/' + self.ID)

                if check_list[0][-4:] != '.png':
                    ID = self.ID + '_' + self.status
                else:
                    ID = self.ID
                if self.frame > len(db.animation_database[ID]) - 1:
                    self.frame = 0

                self.change_status(self.status)
                frame_path = db.animation_database[str(ID)][self.frame]
                frame_img = pygame.image.load(frame_path).convert()
                frame_img.set_colorkey([0, 0, 0])
                self.rect = pygame.Rect(self.pos[0], self.pos[1], frame_img.get_width(), frame_img.get_height())
                if draw:
                    surface.blit(pygame.transform.flip(frame_img, self.flip, False), pos)
            elif self.ID + '.png' in obj_list:
                self.frame = 0
                ID = self.ID
                obj_img = pygame.image.load(self.obj_path + '/' + ID + '.png')
                self.rect = pygame.Rect(self.pos[0], self.pos[1], obj_img.get_width(), obj_img.get_height())
                if draw:
                    surface.blit(obj_img, pos)

        self.frame += round(1 * db.multiply_factor)

    def one_time(self, status, offset=[0, 0]) -> None:
        self.offset = offset
        obj_list = os.listdir(self.obj_path)
        if self.ID in obj_list:
            ID = self.ID
        else:
            check_list = os.listdir(self.animation_path + '/' + self.ID)
            if check_list[0][-4:] != '.png':
                ID = self.ID + '_' + status
            else:
                ID = self.ID

        if self.frame == len(db.animation_database[ID]) - 1:
            self.frame = 0

    def change_status(self, entity_new_status, flip = False) -> None:
        self.flip = flip
        if self.status != entity_new_status:
            self.status = entity_new_status
            self.frame = 0

    def change_offset(self, offset) -> None:
        self.offset = offset

    def get_rect(self) -> pygame.Rect:

        obj_list = os.listdir(self.obj_path)
        if self.ID + '.png' in obj_list:
            frame_path = db.obj_database[self.ID]
            frame_img = pygame.image.load(frame_path).convert()
            return pygame.Rect(self.pos[0], self.pos[1], frame_img.get_width(), frame_img.get_height())
        else:
            try:
                check_list = os.listdir(self.animation_path + '/' + self.ID)
            except:
                check_list = os.listdir(self.animation_path + '/entity/' + self.ID)

            if check_list[0][-4:] != '.png':
                ID = self.ID + '_' + self.status
            else:
                ID = self.ID

            frame_path = db.animation_database[ID][0]
            frame_img = pygame.image.load(frame_path).convert()
            return pygame.Rect(self.pos[0], self.pos[1], frame_img.get_width(), frame_img.get_height())