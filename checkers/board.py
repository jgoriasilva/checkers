from sqlite3 import SQLITE_IGNORE
import pygame
from .constants import BLACK, RED, WHITE, ROWS, COLS, SQUARE_SIZE
from .piece import Piece

class Board():

    def __init__(self):
        self.board = []
        self.create_pieces()

    def draw_squares(self, win: pygame.Surface):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, 8, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_pieces(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col%2 == (row + 1)%2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def draw_pieces(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(win)

    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col) -> Piece:
        return self.board[row][col]
