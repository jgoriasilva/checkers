from xmlrpc.client import Boolean
import pygame
from .board import Board
from .piece import Piece
from .constants import *

class Game():

    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.selected = None
        self.turn = RED
    
    def update(self):
        win = self.win
        selected = self.selected

        self.board.draw_squares(win)
        self.board.draw_pieces(win)

        if selected:
            self.board.draw_valid_moves(win)
            self.board.draw_selected(win, selected)

    def change_turn(self):
        self.turn = WHITE if self.turn == RED else RED

    def select(self, row, col):
        if self.selected is not None:
            result = self.__move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            piece = self.board.get_piece(row, col)
            if piece is not None and piece.color == self.turn:
                self.selected = piece
                self.board.valid_moves = self.board.get_valid_moves(piece)

    def __move(self, target_row, target_col):
        
        valid_moves = self.board.valid_moves
        target_move = (target_row, target_col)
        target = self.board.get_piece(target_row, target_col)
        if self.selected is not None and target is None and target_move in valid_moves:
            skipped = valid_moves[target_move]
            self.board.move_piece(self.selected, target_row, target_col, skipped)
            self.change_turn()
            self.selected = None
        else:
            return False

        return True

    def is_game_over(self):
        return self.board.is_board_over()

    def reset_game(self):
        self.board.reset()
        self.selected = None
        self.turn = RED

    def show_popup(self, text):
        win = self.win
        font = pygame.font.SysFont(None, 30)
        text = font.render(text, True, WHITE)
        rect = text.get_rect()
        rect.center = (WIDTH/2, HEIGHT/2)

        pygame.draw.rect(win, BLACK, (100, 100, 200, 100))
        win.blit(text, rect)