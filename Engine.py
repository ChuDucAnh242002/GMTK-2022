import pygame
import engine.database as db
from engine.map import map
from engine.camera import camera

class Engine():
    def __init__(self, WINDOWN_SIZE, SCALE, FPS):
        self.WINDOWN_SIZE = WINDOWN_SIZE
        self.SCALE = SCALE
        self.FPS = FPS

        db.database(FPS)
        self.map = map()
        self.map.load_map('level_1')
        self.player = None
        self.camera = camera(WINDOWN_SIZE, SCALE)
        self.screen = pygame.display.set_mode(WINDOWN_SIZE)
        self.display = pygame.Surface([WINDOWN_SIZE[0] / SCALE, WINDOWN_SIZE[1] / SCALE])

    def update(self):
        self.player = self.map.update(self.camera.rect)
        self.camera.update(self.player, self.display)

    def render(self):
        self.update()

        self.display.fill([0, 0, 0])

        self.map.render(self.display, self.camera)
        self.entity_render(self.display, self.camera)
        self.object_render(self.display, self.camera)
        self.player.render(self.display, self.camera)

        surf = pygame.transform.scale(self.display, self.WINDOWN_SIZE)
        self.screen.blit(surf, [0, 0])

    def object_render(self, surface, camera):
        for obj in db.objects:
            if obj.rect.colliderect(camera.rect):
                obj.render(surface, camera)

    def entity_render(self, surface, camera):
        for enti in db.entities:
            if enti.rect.colliderect(camera.rect):
                enti.render(surface, camera)
