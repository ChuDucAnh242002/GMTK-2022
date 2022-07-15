"""
    Credits: Dafluffy potato
    Youtube: https://www.youtube.com/c/DaFluffyPotato
"""

import pygame, sys

from pygame.locals import *
from core_funcs import *
# from color import *

pygame.init()

WIDTH, HEIGHT = 768, 432
win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Spritesheet generation")

CLOCK = pygame.time.Clock()
FPS = 60

SCALE = 3
COLORKEY = WHITE
FORCE_BG = WHITE

def generate_borders(base_range, img):
    """
    param: base_range [mouse_pos, mouse_pos]
    param: img
    return: corners
    """
    corners = [
        [min(base_range[0][0], base_range[1][0]), min(base_range[0][1], base_range[1][1])],
        [max(base_range[0][0], base_range[1][0]), min(base_range[0][1], base_range[1][1])],
        [max(base_range[0][0], base_range[1][0]), max(base_range[0][1], base_range[1][1])],
        [min(base_range[0][0], base_range[1][0]), max(base_range[0][1], base_range[1][1])]
    ]
    min_0 = min(base_range[0][0], base_range[1][0])
    min_1 = min(base_range[0][1], base_range[1][1])
    max_0 = max(base_range[0][0], base_range[1][0])
    max_1 = max(base_range[0][1], base_range[1][1])
    corners = [
        [min_0, min_1], # top left
        [max_0, min_1], # bottom left
        [max_0, max_1], # bottom right
        [min_0, max_1] # top right
    ]

    while True:
        full_clear = True
        clear = True
        # top
        for j in range(corners[1][0] - corners[0][0] + 1):
            c = img.get_at((corners[0][0] + j, corners[0][1]))
            c = (c[0], c[1], c[2])
            if c != COLORKEY:
                clear = False
                full_clear = False
        if not clear:
            corners[0][1] -= 1
            corners[1][1] -= 1

        clear = True   
        # right
        for j in range(corners[2][1] - corners[1][1] + 1):
            c = img.get_at((corners[1][0], corners[1][1] + j))
            c = (c[0], c[1], c[2])
            if c != COLORKEY:
                clear = False
                full_clear = False
        if not clear:
            corners[1][0] += 1
            corners[2][0] += 1

        clear = True
        # bottom
        for j in range(corners[2][0] - corners[3][0] + 1):
            c = img.get_at((corners[3][0] + j, corners[3][1]))
            c = (c[0], c[1], c[2])
            if c != COLORKEY:
                clear = False
                full_clear = False
        if not clear:
            corners[2][1] += 1
            corners[3][1] += 1

        clear = True
        # left
        for j in range(corners[3][1] - corners[0][1] + 1):
            c = img.get_at((corners[0][0], corners[0][1] + j))
            c = (c[0], c[1], c[2])
            if c != COLORKEY:
                clear = False
                full_clear = False
        if not clear:
            corners[0][0] -= 1
            corners[3][0] -= 1

        if full_clear:
            break    
    return corners

def generate_tileset(clip_sections, img):
    rect_form_clips = []
    # print(clip_sections)
    for sec in clip_sections:
        row = sec[0]
        while row >= len(rect_form_clips):
            rect_form_clips.append([])
        sec = sec[1]
        rect = pygame.Rect(sec[0][0] + 1, sec[0][1] + 1, sec[2][0] - sec[0][0] - 1, sec[2][1] - sec[0][1] - 1)
        rect_form_clips[row].append(rect)
    # print(rect_form_clips)

    max_width = 0
    height = 0
    for row in rect_form_clips:
        width = sum([sec.width + 2 for sec in row]) + 1
        height += max([sec.height + 2 for sec in row])
        max_width = max(width, max_width)

    print(max_width, height)
    tileset_surf = pygame.Surface((max_width, height))
    tileset_surf.fill(FORCE_BG)
    y = 0
    for row in rect_form_clips:
        tileset_surf.set_at((0, y), (255, 255, 0))
        x = 1 
        for sec in row:
            sec_img = clip(img, sec.x, sec.y, sec.width, sec.height)
            if FORCE_BG:
                sec_img.set_colorkey(COLORKEY)
            tileset_surf.blit(sec_img, (x + 1 , y + 1))
            tileset_surf.set_at((x, y), (255, 0, 255))
            tileset_surf.set_at((x + sec.width+ 1, y), (0, 255, 255))
            tileset_surf.set_at((x, y + sec.height + 1), (0, 255, 255))
            x += sec.width + 2
        y += max([sec.height + 2 for sec in row])
    return tileset_surf

def generate_tileset_1(clip_sections, img):
    """
    clip sections are from each row
    sec[0] is row, sec[1] is four corner pos (left up, right up, right down, left down)
    img is intial image
    """
    rect_form_clips = []
    for sec in clip_sections:
        row = sec[0]
        while row >= len(rect_form_clips):
            rect_form_clips.append([])
        sec = sec[1]
        x = sec[0][0] + 1
        y = sec[0][1] + 1
        tile_width = sec[2][0] - sec[0][0] - 1
        tile_height = sec[2][1] - sec[0][1] - 1
        rect = pygame.Rect(x, y, tile_width, tile_height)
        rect_form_clips[row].append(rect)

    # Calculate width and height of the tileset surf
    max_width = 0
    height = 1
    for row in rect_form_clips:
        width = sum([sec.width + 1 for sec in row]) + 1
        height += max([sec.height + 1 for sec in row])
        max_width = max(width, max_width)

    tileset_surf = pygame.Surface((max_width, height))
    tileset_surf.fill(FORCE_BG)
    
    for y, row in enumerate(rect_form_clips):
        for x, sec in enumerate(row):
            sec_img = clip(img, sec.x, sec.y, sec.width, sec.height)
            if FORCE_BG:
                sec_img.set_colorkey(COLORKEY)
            tileset_surf.blit(sec_img, (x * (sec.width + 1) + 1 , y * (sec.height + 1) + 1))
            tileset_surf.set_at((0, y * (sec.height + 1)), YELLOW)
            tileset_surf.set_at((x * (sec.width + 1) + 1, y * (sec.height + 1)), PINK)
    return tileset_surf

def main():

    path = input('path to image: ')
    img = pygame.image.load(path).convert()
    display_dim = [img.get_width() * SCALE, img.get_height() * SCALE]
    win = pygame.display.set_mode(display_dim, 0, 32)
    dis = img.copy()

    run = True
    clicking = None
    genned_tileset = None

    clip_sections = []
    current_row = 0
    generate_mode = False
    save_count = 0

    while run:
        dis.fill(BLACK)
        if not generate_mode:
            dis.blit(img, (0, 0))

            mx, my = pygame.mouse.get_pos()
            mx = mx //SCALE
            my = my //SCALE

            for sec in clip_sections:
                c = (255, 0, 255)
                if sec[0] != current_row:
                    c = (0, 255, 255)
                pygame.draw.polygon(dis, c, sec[1], 1)

            if clicking:
                click_rect = pygame.Rect(clicking[0], clicking[1], mx-clicking[0], my-clicking[1])
                pygame.draw.rect(dis, (255, 0, 255), click_rect, 1)

        else:
            dis.blit(genned_tileset, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    quit()
                # Ctrl + Z
                if event.key == K_z:
                    if len(clip_sections):
                        clip_sections.pop(-1)
                # Move to next row
                if event.key == K_r:
                    current_row += 1
                # Delete clip sections
                if event.key == K_c:
                    clip_sections = []
                # Save image
                if event.key == K_s:
                    pygame.image.save(dis, 'save_' + str(save_count) + '.png')
                    save_count += 1
                # Generate mode
                if event.key == K_g:
                    if not generate_mode:
                        generate_mode = True
                        genned_tileset = generate_tileset_1(clip_sections, img)
                        display_dim = [genned_tileset.get_width() * SCALE, genned_tileset.get_height() * SCALE]
                        win = pygame.display.set_mode(display_dim, 0, 32)
                        dis = genned_tileset.copy()
                    else:
                        generate_mode = False
                        dis = img.copy()
                        display_dim = [img.get_width() * SCALE, img.get_height() * SCALE]
                        win =pygame.display.set_mode(display_dim, 0, 32)

            # Select tile
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicking = [mx, my]
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    # print([clicking, [mx, my]])
                    if clicking != None:
                        clip_sections.append([current_row, generate_borders([clicking, [mx, my]], img)])
                    clicking = None

        win.blit(pygame.transform.scale(dis, display_dim), (0, 0))
        pygame.display.update()
        CLOCK.tick(FPS)
        
def quit():
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
