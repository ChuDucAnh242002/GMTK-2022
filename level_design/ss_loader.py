"""
    Credits: Dafluffy potato
    Youtube: https://www.youtube.com/c/DaFluffyPotato
"""

import pygame, os, json
from core_funcs import *

pygame.init()
pygame.display.init()

COLORKEY = WHITE

# Load each spritesheet
def load_spritesheet(spritesheet):
    rows = []
    spritesheet_dat = []
    for y in range(spritesheet.get_height()):
        c = spritesheet.get_at((0, y))
        c = (c[0], c[1], c[2])
        if c == YELLOW:
            rows.append(y)
            
    for row in rows:
        row_content = []
        for x in range(spritesheet.get_width()):
            c = spritesheet.get_at((x, row))
            c = (c[0], c[1], c[2])
            if c == PINK: # found tile
                x2 = 0
                while True:
                    x2 += 1
                    c = spritesheet.get_at((x + x2, row))
                    c = (c[0], c[1], c[2])
                    if c == CYAN:
                        break
                y2 = 0
                while True:
                    y2 += 1
                    c = spritesheet.get_at((x, row + y2))
                    c = (c[0], c[1], c[2])
                    if c == CYAN:
                        break
                img = clip(spritesheet, x + 1, row + 1, x2 - 1, y2 - 1)
                img.set_colorkey(COLORKEY)
                row_content.append(img)
        # image for each row
        spritesheet_dat.append(row_content)
    return spritesheet_dat

def load_spritesheet_1(spritesheet, tile_size):
    """
    Param: full tileset image
    return: dict with num of each tile
    """
    rows = []
    spritesheet_dat = {}
    for y in range(spritesheet.get_height()):
        c = spritesheet.get_at((0, y))
        c = (c[0], c[1], c[2])
        if c == YELLOW:
            rows.append(y)

    num = 0 
    for row in rows:
        # row_content = []
        for x in range(spritesheet.get_width()):
            c = spritesheet.get_at((x, row))
            c = (c[0], c[1], c[2])
            if c == PINK:
                img = clip(spritesheet, x, row + 1, tile_size[0], tile_size[1])
                img.set_colorkey(COLORKEY)
                # row_content.append(img)
                spritesheet_dat[num] = img
                num += 1
        # image for each row
        # spritesheet_dat.append(row_content)
    return spritesheet_dat

# load spritesheets based on path
def load_spritesheets(path, tile_size):
    # list of img name in path
    spritesheet_list = os.listdir(path)
    spritesheets = {}
    # spritesheets_data = {}
    for img_file in spritesheet_list:
        # find png
        file_type = img_file.split('.')[-1]
        if file_type == 'png':
            file_path = path + '/' + img_file
            # Example: tiles
            file_name = img_file.split('.')[0]
            spritesheet_dat = load_spritesheet_1(pygame.image.load(file_path), tile_size)
            spritesheets[file_name] = spritesheet_dat

    # spritesheets is a dict: filename and spritesheet data 
    return spritesheets
    
def get_img(spritesheets, pos):
    """
    param: image position
    """
    return spritesheets[pos[0]][pos[1]][pos[2]]

# load_spritesheets("assets/images/tileset")