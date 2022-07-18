import pygame, json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Ink pink
PINK_1 = (254, 108, 144)
PINK_2 = (108, 55, 145)
PURPLE = (135, 30, 106)
DARK_PURPLE = (69, 36, 89)
PURPLE_BLACK = (38, 13, 52)

COLORKEY = WHITE

# read File
def read_f(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def write_f(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def swap_color(img, old_color, new_color):
    img.set_colorkey(old_color)
    dis = img.copy()
    dis.fill(new_color)
    dis.blit(img, (0, 0))
    return dis

# Cut the image
def clip(dis, x, y, width, height):
    copy_dis = dis.copy()
    clip_rect = pygame.Rect(x, y, width, height)
    copy_dis.set_clip(clip_rect)
    image = dis.subsurface(copy_dis.get_clip())
    return image.copy()

# Return corners of a rect
def rect_corners(points):
    point_1 = points[0]
    point_2 = points[1]
    out_1 = [min(point_1[0], point_2[0]), min(point_1[1], point_2[1])]
    out_2 = [max(point_1[0], point_2[0]), max(point_1[1], point_2[1])]
    return [out_1, out_2]

def corner_rect(points):
    points = rect_corners(points)
    x = points[0][0]
    y = points[0][1]
    width = points[1][0] - points[0][0]
    height = points[1][1] - points[0][1]
    rect = pygame.Rect(x, y, width, height)
    return rect

def points_between_2d(points):
    points = rect_corners(points)
    width = points[1][0] - points[0][0] + 1
    height = points[1][1] - points[0][1] + 1
    point_list = []
    for y in range(height):
        for x in range(width):
            point_list.append([points[0][0] + x, points[0][1] + y])
    return point_list

def angle_to(points):
    pass

# load image from full path
def load_image(path):
    path = path + '.png'
    img = pygame.image.load(path)
    return img

# Map from text
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def load_dict_image(domain, names):
    dict_img = {}
    for name in names:
        img_path = domain + name
        dict_img[name] = load_image(img_path)
    return dict_img

def load_dict_map(domain, names):
    dict_map = {}
    for index, name in enumerate(names):
        map_path = domain + name
        dict_map[index] = load_map(map_path)
    return dict_map

def load_json_data(path):
    path = path + ".json"
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def load_layer(name, path, type):
    json_data = load_json_data(path)
    layers = json_data["layers"]
    for layer in layers:
        if layer["name"] == name:
            if type == "tile":
                return [layer["data2D"], [layer["gridCellWidth"], layer["gridCellHeight"]]]
            elif type == "entity":
                return layer["entities"]

def load_dict_json(domain, level, layers):
    level_map = {}
    map_path = domain + "level_" + str(level)
    for layer in layers:
        if layer.find('tile') != -1:
            level_map[layer] = load_layer(layer, map_path, "tile")
        if layer.find('entity') != -1:
            level_map[layer] = load_layer(layer, map_path, "entity")
    return level_map