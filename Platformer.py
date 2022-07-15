import pygame
import sys
from pygame.locals import *
from Engine import Engine

# Setting enviromental ------------------------------------------------------------------------------------------------------------------ #
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(64)
clock = pygame.time.Clock()

pygame.display.set_caption("Adventure Time !!! Made by DAIOTAKU")

WINDOWN_SIZE = (960, 540)
SCALE = 3
FPS = 60

e = Engine(WINDOWN_SIZE, SCALE, FPS)

while True:

    e.render()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT]:
        e.player.move([-2, 0])
    elif key_pressed[K_RIGHT]:
        e.player.move([2, 0])

    clock.tick(60)

    pygame.display.update()
