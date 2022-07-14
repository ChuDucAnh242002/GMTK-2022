import pygame, sys

from pygame.locals import *
from core_funcs import *
from text import Font
from ss_loader import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

WIDTH, HEIGHT = 768, 432
SCALE = 2
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
DIS = pygame.Surface((WIDTH //SCALE, HEIGHT //SCALE))

CLOCK = pygame.time.Clock()
FPS = 60

font = Font("data/font/small_font.png", WHITE)

def quit():
    pygame.quit()
    sys.exit()

def draw():
    WIN.fill(BLACK)
    DIS.fill(BLACK)
    
def main():
    
    spritesheet_data = load_spritesheets("data/images/tileset", (8, 8))
    # print(spritesheet_data)
    run = True
    while run: 
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()

        draw()

        surf = pygame.transform.scale(DIS, (WIDTH, HEIGHT))
        WIN.blit(surf, (0, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()
