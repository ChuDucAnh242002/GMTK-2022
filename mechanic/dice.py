from tkinter import N
import engine.database as db
import random
from engine.entity import entity

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

        if (self.time_per_frame <= 0):
            self.time_per_frame = self.roll_time / self.speed_roll
            self.index += 1
            if self.index >= len(self.inventory):
                self.index = 0

        element = self.inventory[self.index]
        element.pos = self.pos
        element.render(display, camera)

        self.time_per_frame -= db.delta_time
        self.time -= db.delta_time

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