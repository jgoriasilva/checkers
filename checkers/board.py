from sqlite3 import SQLITE_IGNORE
import pygame
from .constants import BLACK, RED, ROWS, SQUARE_SIZE

class Board():

    def draw_squares(self, win: pygame.Surface):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, 8, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
