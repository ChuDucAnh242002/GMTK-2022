import pygame
import engine.database as db


class camera():
    def __init__(self, WINDOWN_SIZE, SCALE):
        self.WINDOWN_SIZE = WINDOWN_SIZE
        self.SCALE = SCALE

        self.true_scroll = [0, 0]
        self.scroll = [0, 0]
        self.rect = pygame.Rect(self.scroll[0], self.scroll[1], self.WINDOWN_SIZE[0] / self.SCALE, self.WINDOWN_SIZE[1] / self.SCALE)
        self.x = self.rect.x
        self.y = self.rect.y


    def update(self, player, display):
        self.true_scroll[0] += (player.x - self.true_scroll[0] - display.get_width() / 2) * (
                    10 * (db.img_FPS / db.FPS)) * 1 / 20
        self.true_scroll[1] += (player.y - self.true_scroll[1] - display.get_height() / 2) * (
                    10 * (db.img_FPS / db.FPS)) * 1 / 20
        scroll = self.true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        self.scroll = scroll
        
        self.rect = pygame.Rect(
                self.scroll[0] - db.IMG_SIZE * 2, 
                self.scroll[1] - db.IMG_SIZE * 2, 
                self.WINDOWN_SIZE[0] / self.SCALE + db.IMG_SIZE * 4, 
                self.WINDOWN_SIZE[1] / self.SCALE + db.IMG_SIZE * 4)

        self.x = self.scroll[0]
        self.y = self.scroll[1]