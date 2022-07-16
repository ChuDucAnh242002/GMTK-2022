from tkinter import N
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
e.DEBUG = ['show_hitbox', 'hide_tile', 'no_img']
# e.DEBUG = ['no_img']
player = e.load_map(0)

while True:

    e.render_english(str(round(clock.get_fps(), 2)), [e.camera.x, e.camera.y], 'small')
    e.render_english("Elements: " + str(len(player.dice.inventory)), [e.camera.x, e.camera.y + 8], 'small')
    e.render_english("Enegry: " + str(player.energy), [e.camera.x, e.camera.y + 8*2], 'small')
    if player.hold_element == None:
        e.render_english("Holding: None", [e.camera.x, e.camera.y + 8*3], 'small')
    else:
        e.render_english("Holding: " + str(player.hold_element.ID), [e.camera.x, e.camera.y + 8*3], 'small')
    
    
    e.render_english("TEST", [464, 464], 'large')

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_0:
                player.roll()

    for element in player.dice.inventory:
        print(element.ID, end = " ")
    print()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT]:
        player.move([-2, 0])
    if key_pressed[K_RIGHT]:
        player.move([2, 0])
    if key_pressed[K_UP]:
        player.move([0, -2])
    if key_pressed[K_DOWN]:
        player.move([0, 2])
        
    
    e.render()
    clock.tick(60)
    pygame.display.update()