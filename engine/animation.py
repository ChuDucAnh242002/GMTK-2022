import pygame
import os
import engine.database as db

class animation():
    def __init__(self, ID, pos, status):
        self.animation_path = 'data/animation'
        self.entity_path = "data/animation/entity"
        self.obj_path = "data/object"
        self.FPS = db.FPS
        self.img_FPS = 12
        self.frame = 0
        self.ID = ID
        self.status = status
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.offset = [0, 0]
        self.rect = self.get_rect()
        self.flip = False

    def render(self, surface, camera, draw = True) -> None:

        self.x = self.pos[0]
        self.y = self.pos[1]

        scroll = camera.scroll
        pos = [self.pos[0] - scroll[0] + self.offset[0], self.pos[1] - scroll[1] + self.offset[1]]
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
            if draw:
                surface.blit(pygame.transform.flip(frame_img, self.flip, False), pos)
        elif self.ID + '.png' in obj_list:
            self.frame = 0
            ID = self.ID
            obj_img = pygame.image.load(self.obj_path + '/' + ID + '.png')
            if draw:
                surface.blit(obj_img, pos)

        self.frame += 1

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