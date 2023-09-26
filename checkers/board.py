from sqlite3 import SQLITE_IGNORE
import pygame
from .constants import *
from .piece import Piece

class Board():

    def __init__(self):
        self.__init()

    def __init(self):
        self.board = []
        self.valid_moves = {}
        self.count = {WHITE: 0, RED: 0}
        self.create_pieces()

    def draw_squares(self, win: pygame.Surface):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, 8, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_pieces_2(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        # self.board[1][2] = Piece(1, 2, WHITE, True)
        self.board[2][3] = Piece(2, 3, RED)
        self.board[4][3] = Piece(4, 3, RED)
        self.board[5][2] = Piece(5, 2, WHITE, True)
        self.count[RED] = 2
        self.count[WHITE] = 1
        pass

    def create_pieces(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col%2 == (row + 1)%2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                        self.count[WHITE] += 1
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                        self.count[RED] += 1
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

    def draw_valid_moves(self, win):
        for move in self.valid_moves.keys():
            row, col = move
            x = col*SQUARE_SIZE + SQUARE_SIZE//2
            y = row*SQUARE_SIZE + SQUARE_SIZE//2
            pygame.draw.circle(win, BLUE, (x, y), PIECE_RADIUS*0.8)

    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col) -> Piece:
        if not 0 <= row < ROWS or not 0 <= col < COLS:
            return None
        return self.board[row][col]

    def remove_piece(self, pieces):
        for row, col, color in pieces:
            self.count[color] -= 1
            self.board[row][col] = None

    def draw_selected(self, win, selected):

        row, col = selected.row, selected.col
        x, y = calc_xy(row, col)

        pygame.draw.circle(win, GREY, (x, y), PIECE_RADIUS*0.3)

    def reset(self):
        self.__init()