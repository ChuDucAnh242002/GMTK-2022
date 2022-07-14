import engine.database as db
from engine.map import map


class Engine():
    def __init__(self, FPS):
        self.FPS = FPS
        db.database(FPS)
        self.map = map()
        self.map.load_map('level_1')
        self.player = None

    def render(self, surface, scroll, display_rect):
        self.player = self.map.render(surface, scroll, display_rect)
        self.entity_render(surface, scroll, display_rect)
        self.object_render(surface, scroll, display_rect)
        self.player.render(surface, scroll, display_rect)

    def object_render(self, surface, scroll, display_rect):
        for obj in db.objects:
            if obj.rect.colliderect(display_rect):
                obj.render(surface, scroll)

    def entity_render(self, surface, scroll, display_rect):
        for enti in db.entities:
            if enti.rect.colliderect(display_rect):
                enti.render(surface, scroll)
