import pygame
from .board import Board

class Game():

    def __init__(self, win):
        self.win = win
        self.board = Board()
    
    def update(self):
        self.board.draw_squares(self.win)
        self.board.draw_pieces(self.win)