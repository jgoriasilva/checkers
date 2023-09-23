import pygame
from .constants import PIECE_RADIUS, WHITE, RED, SQUARE_SIZE 

class Piece():

    def __init__(self, row, col, color):

        self.x = col*SQUARE_SIZE + SQUARE_SIZE//2
        self.y = row*SQUARE_SIZE + SQUARE_SIZE//2

        self.color = color

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.color, (self.x, self.y), PIECE_RADIUS)