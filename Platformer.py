import pygame
import sys
from pygame.locals import *
from Engine import Engine
import engine.database as db

# Setting enviromental ------------------------------------------------------------------------------------------------------------------ #
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(64)
clock = pygame.time.Clock()

WINDOWN = {
    'SIZE': [960, 540],
    'SCALE': 3,
    'FPS': 60
}

IMG = {
    'SIZE': 8,
    'FPS': 12
}

MAP = {
    'CHUNK_SIZE': 8,
    'TOTAL_LEVEL': 1
}

pygame.display.set_caption("BoBoiGirl")
e = Engine(WINDOWN, IMG, MAP)
# e.DEBUG = ['show_hitbox', 'hide_tile', 'no_img']
e.DEBUG = ['no_img']
e.load_map(0)

while True:

    e.render_english(str(round(clock.get_fps(), 2)), [e.camera.x, e.camera.y], 'small')
    e.render_english("TEST", [464, 464], 'large')

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT]:
        e.player.move([-2, 0])
    if key_pressed[K_RIGHT]:
        e.player.move([2, 0])
    if key_pressed[K_UP]:
        e.player.move([0, -2])
    if key_pressed[K_DOWN]:
        e.player.move([0, 2])
    
    e.render()
    clock.tick(60)
    pygame.display.update()