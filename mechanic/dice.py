import engine.database as db
import random

class dice:
    def __init__(self):
        self.inventory = []

    def add_element(self, object):
        self.inventory.append(object)

    def remove_element(self, object):
        self.inventory.remove(object)
    
    def get_element(self):
        return random.choice(self.inventory)
