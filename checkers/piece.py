import pygame
from .constants import PIECE_RADIUS, WHITE, RED, SQUARE_SIZE , CROWN, ROWS

class Piece():

    def __init__(self, row, col, color):

        self.row = row
        self.col = col
        self.color = color

        self.king = False

        self.calc_pos()

    def calc_pos(self):
        self.x = self.col*SQUARE_SIZE + SQUARE_SIZE//2
        self.y = self.row*SQUARE_SIZE + SQUARE_SIZE//2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

        if row == 0 or row == ROWS and not self.king:
            self.king = True

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.color, (self.x, self.y), PIECE_RADIUS)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))