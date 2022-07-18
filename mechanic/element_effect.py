from lib2to3.refactor import get_all_fix_names
import engine.database as db

class effect():
    def __init__(self):
        self.COLLIDE_TABLE = [
            ['sink', 'die', 'blow', 'block'],
            ['pass', 'die', '3', 'block'],
            ['die', 'pass', 'die', 'block'],
            ['float', 'die', 'die', 'pass'],
            ['sink', '7', 'slow', 'block']
        ]
        self.time = 0

    def get_index(self, element, type):
        if type == 'hold':
            if element == None:
                return 0
            elif 'water' in element.ID:
                return 1
            elif 'fire' in element.ID:
                return 2
            elif 'wind' in element.ID:
                return 3
            elif 'rock' in element.ID:
                return 4
        else:
            if 'water' in element.ID:
                return 0
            elif 'fire' in element.ID:
                return 1
            elif 'wind' in element.ID:
                return 2
            elif 'rock' in element.ID:
                return 3

    def get_effect(self, hold_element, obstacle):
        return self.COLLIDE_TABLE[self.get_index(hold_element, 'hold')][self.get_index(obstacle, 'obstacle')]