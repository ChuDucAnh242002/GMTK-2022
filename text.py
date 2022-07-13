"""
    Credits: Dafluffy potato
    Youtube: https://www.youtube.com/c/DaFluffyPotato
"""

import pygame, sys

from core_funcs import *

# TIENG_VIET = []
# #                                       ă     â    ê     ô     ơ      ư
# VIET_LETTER = ['a', 'e', 'i', 'o', 'u', 'aw', 'aa', 'ee', 'oo', 'ow', 'uw']
# # Sắc huyền nặng hỏi ngã
# DAU = ['s', 'f', 'j', 'r', 'x']
# for letter in VIET_LETTER:
#     for d in DAU:
#         viet = letter + d
#         TIENG_VIET.append(viet)

class Font():
    VOWEL_CHAR = ['a', 'e', 'i', 'o', 'u']
    DOUBLE_CHAR = ['a', 'e', 'o', 'd']
    W_CHAR = ['a', 'o', 'u']
    SPECIAL_CHAR = ['\n', ' ', 'd']
    SPECIAL_CHAR.extend(VOWEL_CHAR)
    FG_COLOR = RED
    BG_COLOR = BLACK

    def __init__(self, path, color):
        self.letters = []
        self.letter_spacing = []
        self.line_height = 0
        self.load_font_img(path, color)
        #                                                                                                                                                                                                                                                                                                                                                                 ă      â      đ    ê     ô    ơ      ư
        self.font_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';','aw', 'aa', 'dd', 'ee', 'oo', 'ow', 'uw']
        # self.font_order.extend(TIENG_VIET)
        self.space_width = self.letter_spacing[0]
        self.base_spacing = 1
        self.line_spacing = 2
        
        # Rendering Vietnamese
        self.x_offset = 0
        self.y_offset = 0
        self.index = 0
        self.char = None
        self.text = None

    def load_font_img(self, path, font_color):
        font_img = pygame.image.load(path).convert()
        font_img = swap_color(font_img, self.FG_COLOR, font_color)
        last_x = 0
        self.line_height = font_img.get_height()
        for x in range(font_img.get_width()):
            # If it is gray
            if font_img.get_at((x, 0))[0] == 127:
                self.letters.append(clip(font_img, last_x, 0, x - last_x, font_img.get_height()))
                self.letter_spacing.append(x - last_x)
                last_x = x + 1
            x += 1
        for letter in self.letters:
            letter.set_colorkey(self.BG_COLOR)
            
    def width(self, text):
        text_width = 0
        for char in text:
            if char == ' ':
                text_width += self.space_width + self.base_spacing
            else:
                text_width += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
        return text_width
    
    def render_english(self, text, dis, pos, line_width = 0):
        x_offset = 0
        y_offset = 0
        if line_width != 0:
            spaces = []
            x = 0
            for i, char in enumerate(text):
                if char == ' ':
                    spaces.append((x, i))
                    x += self.space_width + self.base_spacing
                else:
                    x += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            line_offset = 0
            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]
        for char in text:
            if char not in ['\n', ' ']:
                dis.blit(self.letters[self.font_order.index(char)], (pos[0] + x_offset, pos[1] + y_offset))
                x_offset += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            elif char == ' ':
                x_offset += self.space_width + self.base_spacing
            else:
                y_offset += self.line_spacing + self.line_height
                x_offset = 0

    def render_viet(self, text, dis, pos, line_width = 0):
        self.x_offset = 0
        self.y_offset = 0
        self.index = 0
        self.text = text
        if line_width != 0:
            spaces = []
            x = 0
            for i, char in enumerate(text):
                if char == ' ':
                    spaces.append((x, i))
                    x += self.space_width + self.base_spacing
                else:
                    x += self.letter_spacing[self.font_order.index(char)] + self.base_spacing
            line_offset = 0
            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]

        while self.index < len(self.text):
            self.char = self.text[self.index]
            self.index += 1
            if self.char not in self.SPECIAL_CHAR:
                self.draw_char(dis, pos)
                continue
            elif self.char == ' ':
                self.x_offset += self.space_width + self.base_spacing
                continue
            elif self.char == '\n':
                self.y_offset += self.line_spacing + self.line_height
                self.x_offset = 0
                continue

            if self.index < len(self.text):
                # â, đ, ê, ô
                if self.char in self.DOUBLE_CHAR:
                    next_char = self.text[self.index]
                    if next_char == self.char:
                        self.next(next_char)
                        if self.char != 'dd':
                            self.check_dau()
                        self.draw_char(dis, pos)
                        continue

                # ă, ư, ơ
                if self.char in self.W_CHAR:
                    next_char = self.text[self.index]
                    if next_char == 'w':
                        self.next(next_char)
                        self.check_dau()
                        self.draw_char(dis, pos)
                        continue

                # Dau for vowel
                if self.char in self.VOWEL_CHAR:
                    self.check_dau()
                    self.draw_char(dis, pos)
                    continue

            self.draw_char(dis, pos)
            
    def draw_char(self, dis, pos):
        dis.blit(self.letters[self.font_order.index(self.char)], (pos[0] + self.x_offset, pos[1] + self.y_offset))
        self.x_offset += self.letter_spacing[self.font_order.index(self.char)] + self.base_spacing    

    def next(self, next_char):
        self.char = self.char + next_char
        self.index += 1

    # def check_dau(self):
    #     if self.index < len(self.text):
    #         next_char = self.text[self.index]
    #         if next_char in DAU:
    #             self.next(next_char)

