from dis import dis
from msilib.schema import Directory
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
        self.block = []

    def update(self):
        self.update_effect()
        super().update()
        self.update_status()
        self.collect_element()
        self.dice.update(self.pos)

    def update_status(self):
        
        if self.rolling:
            hold_temp = self.dice.get_element()
            if (hold_temp != None):
                self.hold_element = hold_temp
                self.rolling = False


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

        directions = ['up', 'down', 'left', 'right', 'surround']

        for direc in directions:
            for element in self.near_by[direc]:
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
                self.block = []
                self.change_status('die')
                if self.frame >= len(db.animation_database[self.ID + '_' + self.status]):
                    if self.hold_element == None:
                        self.change_status('normal')
                    else:
                        self.change_status(self.hold_element.ID[:len(self.hold_element.ID) - len('_element')])
                    self.rect.x, self.rect.y = self.spawn_pos.copy()
                    self.x, self.y = self.spawn_pos.copy()
                    self.pos = self.spawn_pos.copy()
                    self.list_effects = []
                return

            if effect == 'none':
                self.effect.time = 0
                self.block = []

            if effect.isnumeric():
                self.block = []
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
                    self.block.append(obstacle.rect)
                elif effect == 'slow':
                    self.friction = [1, 1]
                    self.block = []
                elif effect == 'blow':
                    self.block = []
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
                    if self.status != 'jump':
                        self.rect.y = obstacle.rect.y - self.rect.height / 2

    def collide_test(self) -> list:
        hit_list = []
        db.tile_rects += self.block
        self.block = []
        for tile in db.tile_rects:
            if self.rect.colliderect(tile) and tile != self.rect:
                hit_list.append(tile)
        return hit_list

    def move(self, movement) -> None:

        movement = [round(movement[0] * db.multiply_factor), round(movement[1] * db.multiply_factor)]
        self.collision = {'top': False, 'bottom': False, 'right': False, 'left': False}

        # Update location x ---------------------------------------------------------------------------------------------------- #
        if movement[0] >= self.friction[0]:
            movement[0] -= self.friction[0]
        elif movement[0] < -self.friction[0]:
            movement[0] += self.friction[0]
        else:
            movement[0] = 0

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
        if movement[1] <= -self.friction[1]:
            movement[1] += self.friction[1]
        elif movement[1] > self.friction[1]:
            movement[1] -= self.friction[1]
        else:
            movement[1] = 0
        
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

        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

        self.pos = [self.x, self.y]
