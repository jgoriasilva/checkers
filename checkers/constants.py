import pygame
import random

# board
HEIGHT, WIDTH = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT//ROWS
PIECE_RADIUS = SQUARE_SIZE//2 - 10

# rgb
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (45,25))

KING_SCORE = 0.5

def calc_xy(row, col):
    x = col*SQUARE_SIZE + SQUARE_SIZE//2
    y = row*SQUARE_SIZE + SQUARE_SIZE//2

    return x, y

def shuffle_dict(d):
    shuffled_dict = {}

    keys_list = list(d.keys())
    random.shuffle(keys_list)

    for key in keys_list:
        v = d[key]
        if type(v) is not list:
            v = shuffle_dict(v)
        shuffled_dict[key] = v

    return shuffled_dict