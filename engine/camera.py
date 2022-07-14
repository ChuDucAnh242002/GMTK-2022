import pygame
import engine.database as db


class camera():
    def __init__(self, WINDOWN_SIZE, SCALE):
        self.WINDOWN_SIZE = WINDOWN_SIZE
        self.SCALE = SCALE

        self.true_scroll = [0, 0]
        self.scroll = [0, 0]
        self.rect = pygame.Rect(self.scroll[0], self.scroll[1], self.WINDOWN_SIZE[0] / self.SCALE, self.WINDOWN_SIZE[1] / self.SCALE)


    def update(self, player, display):
        self.true_scroll[0] += (player.x - self.true_scroll[0] - display.get_width() / 2) * (
                    10 * (db.img_FPS / db.FPS)) * 1 / 20
        self.true_scroll[1] += (player.y - self.true_scroll[1] - display.get_height() / 2) * (
                    10 * (db.img_FPS / db.FPS)) * 1 / 20
        scroll = self.true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        self.scroll = scroll
        self.rect = pygame.Rect(self.scroll[0], self.scroll[1], self.WINDOWN_SIZE[0] / self.SCALE, self.WINDOWN_SIZE[1] / self.SCALE)