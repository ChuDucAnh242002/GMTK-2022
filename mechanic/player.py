from dis import dis
from re import S
import engine.database as db
from engine.entity import entity
from mechanic.dice import dice
from mechanic.element_effect import effect

class player(entity):
    def __init__(self, ID, pos, status = 'normal', tag = ['entity', 'player']):
        super().__init__(ID, pos, status, tag)

        self.dice = dice(self.pos)
        self.energy = 0
        self.hold_element = None
        self.effect = effect()
        self.list_effects = []
        self.rolling = False

    def update(self):
        super().update()
        self.update_status()
        self.collect_element()
        self.update_effect()
        self.dice.update(self.pos)

    def update_status(self):
        
        if self.rolling:
            hold_temp = self.dice.get_element()
            if (hold_temp != None):
                self.hold_element = hold_temp
                self.rolling = False

        if self.hold_element == None:
            self.change_status('normal')
        elif 'water' in self.hold_element.ID:
            self.change_status('water')
        elif 'wind' in self.hold_element.ID:
            self.change_status('wind')
        elif 'stone' in self.hold_element.ID:
            self.change_status('stone')
        elif 'fire' in self.hold_element.ID:
            self.change_status('fire')


    def render(self, display, camera):
        super().render(display, camera)
        self.dice.render(display, camera)
        self.list_effects = []
        self.update()

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
            self.rolling = True
            self.energy -= 1
            hold_temp = self.dice.get_element()
            
            if (hold_temp != None):
                self.hold_element = hold_temp
                self.rolling = False


    def update_effect(self):
        self.list_effects.append('none')
        for element in self.near_by['surround']:
            if element != 'tile':
                if 'element' not in element.ID:
                    if element.ID in ['water', 'fire', 'wind', 'stone']:
                        if ('none' in self.list_effects):
                            self.list_effects = []
                        self.list_effects.append([element, self.effect.get_effect(self.hold_element, element)])

        self.apply_effect()

    def apply_effect(self):
        self.friction = [0, 0]

        for data in self.list_effects:
            effect = data[1]
            obstacle = data[0]

            if effect == 'die':
                self.rect.x, self.rect.y = self.spawn_pos.copy()
                return

            if effect == 'none':
                self.effect.time = 0

            if effect.isnumeric():
                if self.effect.time > 0:
                    self.effect.time -= db.delta_time
                    if self.effect.time <= 0:
                        self.rect.x, self.rect.y = self.spawn_pos.copy()
                        self.list_effects = []
                        self.effect.time = 0
                else:
                    self.effect.time = int(effect)
            else:
                self.effect.time = 0
                if effect == 'block':
                    db.add_tile(obstacle.rect)
                elif effect == 'slow':
                    self.friction = [1, 1]
                elif effect == 'blow':
                    power = 200
                    for _ in range(power):
                        if obstacle in self.near_by['left']:
                            self.move([1, 0])
                        if obstacle in self.near_by['right']:
                            self.move([-1, 0])
                        if obstacle in self.near_by['up']:
                            self.move([0, 1])
                        if obstacle in self.near_by['down']:
                            self.move([0, -1])
                elif effect == 'float':
                    pass
