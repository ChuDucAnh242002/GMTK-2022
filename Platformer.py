from re import T
from tkinter import N
import pygame
import sys
from pygame.locals import *
from Engine import Engine
from engine.core_funcs import BLACK, WHITE
import engine.database as db

# Setting enviromental ------------------------------------------------------------------------------------------------------------------ #
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(64)
clock = pygame.time.Clock()

WINDOWN = {
    'SIZE': [1080, 720],
    'SCALE': 2,
    'FPS': 60
}

IMG = {
    'SIZE': 16,
    'FPS': 12
}

MAP = {
    'CHUNK_SIZE': 8,
}

pygame.display.set_caption("BoBoiGirl")
e = Engine(WINDOWN, IMG, MAP)
# e.DEBUG = ['show_hitbox', 'hide_tile', 'no_img']
# e.DEBUG = ['show_hitbox', 'hide_tile']
# e.DEBUG = ['show_hitbox']
# e.DEBUG = ['show_hitbox', 'no_img']
# e.DEBUG = ['no_img']
player = e.load_map(0)

gravity = 0

while True:

    e.render_english(str(round(clock.get_fps(), 2)), [e.camera.x, e.camera.y], 'small')
    e.render_english("Elements: " + str(len(player.dice.inventory)), [e.camera.x, e.camera.y + 8], 'small')
    e.render_english("Enegry: " + str(player.energy), [e.camera.x, e.camera.y + 8*2], 'small')
    if player.hold_element == None:
        e.render_english("Holding: None", [e.camera.x, e.camera.y + 8*3], 'small')
    else:
        e.render_english("Holding: " + str(player.hold_element.ID), [e.camera.x, e.camera.y + 8*3], 'small')
    
    e.render_english("TEST", [464, 464], 'large')

    player.move([0, gravity])

    gravity += 0.1
    if gravity > 10:
        gravity = 10

    if player.collision['bottom'] or player.collision['top']:
        gravity = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_0:
                if player.rolling == False:
                    player.roll()
            if event.key == K_UP and 'tile' in player.near_by['surround'] and 'tile' in player.near_by['down']:
                gravity = -2.5

                if player.hold_element != None:
                    if 'wind' in player.hold_element.ID:
                        gravity = -3.5
                    elif 'stone' in player.hold_element.ID:
                        gravity = -2

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT]:
        player.move([-3, 0])
    if key_pressed[K_RIGHT]:
        player.move([3, 0])
    
    if key_pressed[K_1]:
        player.hold_element.ID = 'water_element'
    if key_pressed[K_2]:
        player.hold_element.ID = 'fire_element'
    if key_pressed[K_3]:
        player.hold_element.ID = 'wind_element'
    if key_pressed[K_4]:
        player.hold_element.ID = 'stone_element'
    
    e.render(BLACK)

    clock.tick(60)
    pygame.display.update()