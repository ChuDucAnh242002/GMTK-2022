from tkinter import N
import engine.database as db
import random
import pygame
from engine.core_funcs import *

class dice:
    def __init__(self, pos):
        self.inventory = []
        self.pos = pos
        
        self.roll = False
        self.roll_time = 2 + random.randint(0, 10)/10
        self.speed_roll = random.randint(10, 20)

        self.time = 0
        self.time_per_frame = self.roll_time / self.speed_roll
        self.index = 0
        
        self.rolled_element = None

    def update(self, pos):
        self.pos[0] = pos[0] + 5
        self.pos[1] = pos[1] - 50

    def render(self, display, camera):
        
        if not self.roll:
            return

        scroll = camera.scroll
        pos = [self.pos[0] - scroll[0], self.pos[1] - scroll[1]]

        if self.index >= len(db.animation_database['dice_roll']):
            self.index = 0
        
        ID = 'dice_roll'
        frame_path = db.animation_database[str(ID)][self.index]
        frame_img = pygame.image.load(frame_path).convert()
        frame_img.set_colorkey(COLORKEY)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], frame_img.get_width(), frame_img.get_height())
        display.blit(pygame.transform.flip(frame_img, False, False), pos)

        self.time_per_frame -= db.delta_time
        self.time -= db.delta_time

        self.index += 2


    def add_element(self, object):
        self.inventory.append(object)

    def remove_element(self, object):
        self.inventory.remove(object)
    
    def get_element(self):
        if not self.roll:
            self.rolled_element = None
            
            self.roll = True
            self.time = self.roll_time
            self.time_per_frame = self.roll_time / self.speed_roll
        
        if self.roll and self.time <= 0:
            self.roll = False
            
            if self.index >= len(self.inventory):
                self.index = 0

            self.rolled_element = self.inventory[self.index]
            self.remove_element(self.rolled_element)
        
        return self.rolled_element