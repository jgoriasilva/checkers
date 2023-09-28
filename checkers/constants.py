import pygame

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