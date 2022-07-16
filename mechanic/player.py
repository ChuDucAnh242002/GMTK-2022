import engine.database as db
from engine.entity import entity
from mechanic.dice import dice
from mechanic.element_effect import effect

class player(entity):
    def __init__(self, ID, pos, status = 'idle', tag = ['entity', 'player']):
        super().__init__(ID, pos, status, tag)
        self.dice = dice()
        self.energy = 0
        self.hold_element = None

    def update(self):
        super().update()
        self.collect_element()

    def render(self, display, camera):
        self.update()
        super().render(display, camera)

    def collect_element(self):
        for object in self.near_by['surround']:
            if object != 'tile':
                if 'element' in object.ID:
                    self.dice.add_element(object)
                    db.remove_object(object)
                if 'energy' in object.ID:
                    self.energy += 1
                    db.remove_object(object)

    def roll(self):
        if len(self.dice.inventory) > 0 and self.energy > 0:
            self.energy -= 1
            self.hold_element = self.dice.get_element()
            self.dice.remove_element(self.hold_element)