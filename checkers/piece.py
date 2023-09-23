import pygame
from .constants import PIECE_RADIUS, WHITE, RED, SQUARE_SIZE , CROWN

class Piece():

    def __init__(self, row, col, color):

        self.x = col*SQUARE_SIZE + SQUARE_SIZE//2
        self.y = row*SQUARE_SIZE + SQUARE_SIZE//2

        self.color = color

        self.king = False

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.color, (self.x, self.y), PIECE_RADIUS)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))