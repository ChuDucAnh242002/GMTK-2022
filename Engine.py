import pygame
import time
import engine.database as db
from engine.map import map
from engine.camera import camera
from engine.core_funcs import *
from engine.text import Font

class Engine():
    def __init__(self, WINDOWN, IMG, MAP):
        self.WINDOWN_SIZE = WINDOWN['SIZE']
        self.SCALE = WINDOWN['SCALE']

        db.database(WINDOWN['FPS'], IMG['FPS'])
        db.CHUNK_SIZE = MAP['CHUNK_SIZE']
        
        self.FPS = db.FPS


        self.map = map(MAP['TOTAL_LEVEL'])
        self.player = None

        self.screen = pygame.display.set_mode(WINDOWN['SIZE'])
        self.display = pygame.Surface([self.WINDOWN_SIZE[0] / self.SCALE, self.WINDOWN_SIZE[1] / self.SCALE])
        self.camera = camera(WINDOWN['SIZE'], WINDOWN['SCALE'])

        self.prev_time = time.time()
        self.now_time = 0
        self.delta_time = 0
        self.multiply_factor = 0
        self.DEBUG = []

        # { 'TEXT' : [pos, path, color, language] }
        self.text = {}

    def load_map(self, level):
        self.map.load_map(level)
        self.update()

    def update(self):
        db.DEBUG = self.DEBUG
        self.player = self.map.update(self.camera)
        self.camera.update(self.player, self.display)

    def clean(self):
        self.text = {}
        db.object_camera = []
        db.entity_camera = []

    def render(self):
        self.update()

        self.map.render(self.display, self.camera)
        self.entity_render(self.display, self.camera)
        self.object_render(self.display, self.camera)
        self.font_render()
        self.player.render(self.display, self.camera)

        if 'show_hitbox' in self.DEBUG:
            for rect in db.tile_rects:
                pygame.draw.rect(self.display, YELLOW, [rect.x - self.camera.scroll[0], rect.y - self.camera.scroll[1], rect.width, rect.height], 1)

            direction = ['left', 'right', 'up', 'down', 'surround']
            for direc in direction:
                rect = self.player.get_nearby_rect(direc)
                pygame.draw.rect(self.display, GREEN, [rect.x - self.camera.scroll[0], rect.y - self.camera.scroll[1], rect.width, rect.height], 1)


        surf = pygame.transform.scale(self.display, self.WINDOWN_SIZE)
        self.screen.blit(surf, [0, 0])

        self.now_time = time.time()
        db.delta_time = self.now_time - self.prev_time
        self.delta_time = db.delta_time
        self.prev_time = self.now_time

        db.multiply_factor = db.delta_time * db.FPS
        self.multiply_factor = db.multiply_factor
        
        self.display.fill([0, 0, 0])
        self.clean()

    def object_render(self, surface, camera):
        for object in db.objects:
            if object.rect.colliderect(camera.rect):
                object.render(surface, camera)
                db.object_camera.append(object)

    def entity_render(self, surface, camera):
        for entity in db.entities:
            if entity.rect.colliderect(camera.rect):
                entity.render(surface, camera)
                db.entity_camera.append(entity)

    def font_render(self):
        for text in self.text:
            pos = self.text[text][0]
            path = self.text[text][1]
            color = self.text[text][2]
            lang = self.text[text][3]

            font = Font(path, color)
            if lang == 'english':
                font.render_english(text, self.display, pos)
            elif lang == 'viet':
                font.render_viet(text, self.display, pos)

    def render_english(self, text, pos, size = 'small', color = WHITE):
        
        path = 'data/font/' + size + '_font.png'
        pos = [pos[0] - self.camera.scroll[0], pos[1] - self.camera.scroll[1]]
        self.text[text] = [pos, path, color, 'english']
    
    def render_viet(self, text, pos, size = 'small', color = WHITE):
        
        path = 'data/font/' + size + '_font.png'
        pos = [pos[0] - self.camera.scroll[0], pos[1] - self.camera.scroll[1]]
        self.text[text] = [pos, path, color, 'viet']
