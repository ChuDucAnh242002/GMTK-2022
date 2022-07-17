from tkinter import N
import pygame
import sys
from pygame.locals import *
from Engine import Engine
from engine.core_funcs import *
import engine.database as db
import random

# Setting enviromental ------------------------------------------------------------------------------------------------------------------ #
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(64)
clock = pygame.time.Clock()

WINDOWN = {
    'SIZE': [1080, 720],
    'SCALE': 1,
    'FPS': 60
}

IMG = {
    'SIZE': 16,
    'FPS': 3
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
# e.DEBUG = ['show_hitbox', 'show_hitbox_tile', 'hide_tile']


gravity = 0

level = 0
start = True


# Sound for game
fire = pygame.mixer.Sound('data/music/Fire.wav')
fire_play = False
fire.set_volume(0.15)

blow = pygame.mixer.Sound('data/music/Wind Blow.wav')

underwater = pygame.mixer.Sound('data/music/Underwater.wav')
underwater.set_volume(0.2)
underwater_play = False

transform = pygame.mixer.Sound('data/music/Transform sound.wav')

swimming = pygame.mixer.Sound('data/music/Swimming.wav')
swimming_play = False

step = [
    pygame.mixer.Sound('data/music/Step 1.wav'),
    pygame.mixer.Sound('data/music/Step 2.wav'),
    pygame.mixer.Sound('data/music/Step 3.wav')
]
step_choice = None
step_time = 0


steam = pygame.mixer.Sound('data/music/Steam.wav')
steam.set_volume(0.3)
steam.play()

fall = pygame.mixer.Sound('data/music/Rock Fall.wav')
jump = [
    pygame.mixer.Sound('data/music/Jump_1.wav'),
    pygame.mixer.Sound('data/music/Jump_2.wav')
]
jump_choice = None

bg_music =  pygame.mixer.Sound('data/music/First_of_all.mp3')
bg_music.set_volume(0.3)
bg_music.play(-1)

MAX_DISTANCE = 20

SOUND = []

while True:

    if start:
        player = e.load_map(level)
        start = False

    for data in player.near_by['surround']:
        if data != 'tile':
            if data.ID == 'gate':
                start = True
                level += 1
                continue

    obj_ID = []
    for obj in player.near_by['surround']:
        if obj != 'tile':
            obj_ID.append(obj.ID)
    for obj in db.object_camera:
        obj_ID.append(obj.ID)
    
    if 'fire' in obj_ID:
        if fire_play == False:
            fire.play(-1)
            fire_play = True
    else:
        fire.stop()
        fire_play = False

    if 'blow' in player.list_effects:
        blow.play()
    
    if 'float' in player.list_effects:
        if swimming_play == False:
            swimming.play(-1)
            swimming_play = True
    else:
        swimming.stop()
        swimming_play = False

    if 'water' in obj_ID and 'float' not in player.list_effects:
        if underwater_play == False:
            underwater.play()
            underwater_play = True
    else:
        underwater_play = False
        underwater.stop()

    if 'die' in player.list_effects:
        if player.hold_element != 'None':
            if player.hold_element.ID == 'fire' and 'water' in obj_ID:
                steam.play()
            elif player.hold_element.ID == 'water' and 'fire' in obj_ID:
                steam.play()

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

    key_pressed = pygame.key.get_pressed()

    if player.status != 'die':
        if key_pressed[K_LEFT] or key_pressed[K_RIGHT]:
            if step_time == 0:
                step_choice = random.choice(step)
                step_time = 45
                step_choice.set_volume(0.5)
                step_choice.play()
            step_time -= 1
        else:
            if step_choice != None:
                step_choice.stop()


        if not key_pressed[K_LEFT] and not key_pressed[K_RIGHT] and player.status != 'jump':
            if player.hold_element == None:
                player.change_status('normal')
            else:
                player.change_status(player.hold_element.ID[:len(player.hold_element.ID) - len('_element')])
        if player.collision['bottom'] and player.status == 'jump':
            if player.hold_element == None:
                player.change_status('normal')
            else:
                player.change_status(player.hold_element.ID[:len(player.hold_element.ID) - len('_element')])

        if key_pressed[K_UP]:
            if ('tile' in player.near_by['surround'] and 'tile' in player.near_by['down'] and player.status != 'die'):
                gravity = -2.5
                player.change_status('jump')
                jump_choice = random.choice(jump)
                jump_choice.set_volume(0.5)
                jump_choice.play()
                if player.hold_element != None:
                    if 'wind' in player.hold_element.ID:
                        gravity = -3.5
                    elif 'stone' in player.hold_element.ID:
                        gravity = -2
            for data in player.list_effects:
                effect = data[1]
                if effect == 'float':
                    gravity = -2.5
                    player.change_status('jump')
                    jump_choice = random.choice(jump)
                    jump_choice.set_volume(0.5)
                    jump_choice.play()
                if player.hold_element != None:
                    if 'wind' in player.hold_element.ID:
                        gravity = -3.5
                    elif 'stone' in player.hold_element.ID:
                        gravity = -2
                    player.change_status('jump')
                    jump_choice = random.choice(jump)
                    jump_choice.set_volume(0.5)
                    jump_choice.play()

        elif key_pressed[K_LEFT]:
            player.move([-3, 0])
            if player.status != 'jump':
                player.change_status('walk')
        elif key_pressed[K_RIGHT]:
            player.move([3, 0])
            if player.status != 'jump':
                player.change_status('walk')

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_0:
                if player.rolling == False:
                    player.roll()
                    if player.rolling:
                        transform.play()
            elif event.key == K_5:
                start = True
                level += 2


    
    
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