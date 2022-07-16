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

e = Engine(WINDOWN, IMG, MAP)
e.load_map(0)

e.DEBUG = ['show_hitbox', 'hide_tile', 'no_img']

while True:

    pygame.display.set_caption("FPS: " + str(clock.get_fps()))

    e.render()

    # for obj in db.object_camera:
    #     if obj.ID == 'stone' and 'stone' in e.player.near_by['surround']:
    #         if 'stone' in e.player.near_by['right']:
    #             obj.move([2, 0])
    #         elif 'stone' in e.player.near_by['left']:
    #             obj.move([-2, 0])

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT]:
        e.player.move([-2, 0])
    elif key_pressed[K_RIGHT]:
        e.player.move([2, 0])
    elif key_pressed[K_UP]:
        e.player.move([0, -2])
    elif key_pressed[K_DOWN]:
        e.player.move([0, 2])
    
    clock.tick(e.FPS)

    pygame.display.update()
