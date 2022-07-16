import pygame
import time
import engine.database as db
from engine.map import map
from engine.camera import camera

class Engine():
    def __init__(self, WINDOWN_SIZE, SCALE, FPS, img_FPS, total_level):
        self.WINDOWN_SIZE = WINDOWN_SIZE
        self.SCALE = SCALE

        db.database(FPS, img_FPS)
        self.FPS = db.FPS

        self.map = map(total_level)
        self.player = None

        self.screen = pygame.display.set_mode(WINDOWN_SIZE)
        self.display = pygame.Surface([WINDOWN_SIZE[0] / SCALE, WINDOWN_SIZE[1] / SCALE])
        self.camera = camera(WINDOWN_SIZE, SCALE)

        self.prev_time = time.time()
        self.now_time = 0
        self.delta_time = 0
        self.multiply_factor = 0
        self.DEBUG = False

    def load_map(self, level):
        self.map.load_map(level)

    def update(self):
        db.DEBUG = self.DEBUG
        self.player = self.map.update(self.camera)
        self.camera.update(self.player, self.display)

    def render(self):
        self.update()

        self.display.fill([0, 0, 0])

        self.map.render(self.display, self.camera)
        self.entity_render(self.display, self.camera)
        self.object_render(self.display, self.camera)
        self.player.render(self.display, self.camera)

        if (self.DEBUG):

            for entity in db.entity_camera:
                pygame.draw.rect(self.display, [0, 0, 255], [entity.x - self.camera.scroll[0], entity.y - self.camera.scroll[1], entity.width, entity.height], 1)

            for obj in db.object_camera:
                pygame.draw.rect(self.display, [255, 255, 255], [obj.x - self.camera.scroll[0], obj.y - self.camera.scroll[1], obj.width, obj.height], 1)


            for rect in db.tile_rects:
                pygame.draw.rect(self.display, [255, 0, 0], [rect.x - self.camera.scroll[0], rect.y - self.camera.scroll[1], rect.width, rect.height], 1)

            direction = ['left', 'right', 'up', 'down', 'surround']
            for direc in direction:
                rect = self.player.get_nearby_rect(direc)
                pygame.draw.rect(self.display, [0, 255, 0], [rect.x - self.camera.scroll[0], rect.y - self.camera.scroll[1], rect.width, rect.height], 1)


        surf = pygame.transform.scale(self.display, self.WINDOWN_SIZE)
        self.screen.blit(surf, [0, 0])

        self.now_time = time.time()
        db.delta_time = self.now_time - self.prev_time
        self.delta_time = db.delta_time
        self.prev_time = self.now_time

        db.multiply_factor = db.delta_time * db.FPS
        self.multiply_factor = db.multiply_factor

    def object_render(self, surface, camera):
        db.object_camera = []

        for object in db.objects:
            if object.rect.colliderect(camera.rect):
                object.render(surface, camera)
                db.object_camera.append(object)

    def entity_render(self, surface, camera):
        db.entity_camera = []

        for entity in db.entities:
            if entity.rect.colliderect(camera.rect):
                entity.render(surface, camera)
                db.entity_camera.append(entity)
