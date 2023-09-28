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
        self.count_kings = {WHITE: 0, RED: 0}
        # self.create_pieces_2()
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
            pygame.draw.circle(win, BLUE, (x, y), PIECE_RADIUS*0.5)

    def move_piece(self, piece, target_row, target_col):

        self.board[piece.row][piece.col], self.board[target_row][target_col] = self.board[target_row][target_col], self.board[piece.row][piece.col]
        piece.move(target_row, target_col)
        if target_row == 0 or target_row == ROWS-1 and not piece.king:
            piece.make_king()
            self.count_kings[piece.color] += 1

        skipped = self.valid_moves[(target_row, target_col)]
        if len(skipped):
            self.remove_piece(skipped)

    def get_piece(self, row, col) -> Piece:
        if not 0 <= row < ROWS or not 0 <= col < COLS:
            return None
        return self.board[row][col]

    def remove_piece(self, pieces):
        for piece in pieces:
            row, col, color, king = piece.row, piece.col, piece.color, piece.king
            self.count[color] -= 1
            self.board[row][col] = None
            if king:
                self.count_kings[color] -= 1

    def draw_selected(self, win, selected):

        row, col = selected.row, selected.col
        x, y = calc_xy(row, col)

        pygame.draw.circle(win, GREY, (x, y), PIECE_RADIUS*0.3)

    def reset(self):
        self.__init()

    def evaluate(self):
        score_count = self.count[WHITE] - self.count[RED]
        score_kings = (self.count_kings[WHITE] - self.count_kings[RED]) * KING_SCORE

        board_score = score_count + score_kings

        return board_score

    def get_color_pieces(self, color):

        board = self.board
        pieces = [piece for row in board for piece in row if piece and piece.color == color]

        return pieces

    def get_valid_moves(self, piece: Piece):
        moves = {}
        if piece is None:
            return moves
        row, col, color, king = piece.row, piece.col, piece.color, piece.king

        if king:
            moves.update(self.__explore(row, col, color, -1, -1, moves, []))
            moves.update(self.__explore(row, col, color, -1, +1, moves, []))
            moves.update(self.__explore(row, col, color, +1, -1, moves, []))
            moves.update(self.__explore(row, col, color, +1, +1, moves, []))
            
        else:
            direction = +1 if color == WHITE else -1
            moves.update(self.__explore(row, col, color, direction, -1, moves, []))
            moves.update(self.__explore(row, col, color, direction, +1, moves, []))

        return moves

    def __explore(self, row, col, color, direction, side, moves, skipped, skipping=False):
        target_row, target_col = row + direction, col + side

        if skipping:
            moves.update({(row, col): skipped})
        if not 0 <= target_row <= 7 or not 0 <= target_col <= 7:
            return moves

        target_piece = self.get_piece(target_row, target_col)

        if not skipping:
            if target_piece is None:
                moves.update({(target_row, target_col): skipped})
            elif target_piece.color != color:
                destination = self.get_piece(target_row+direction, target_col+side)
                if destination is not None:
                    return moves
                else:
                    skipped_piece = self.get_piece(target_row, target_col)
                    new_skipped = skipped + [skipped_piece]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, +1, moves, new_skipped, True))
        
        else:
            if target_piece is None:
                moves.update({(row, col): skipped})
            elif target_piece.color != color:
                destination = self.get_piece(target_row+direction, target_col+side)
                if destination is not None:
                    return moves
                else:
                    skipped_piece = self.get_piece(target_row, target_col)
                    new_skipped = skipped + [skipped_piece]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, +1, moves, new_skipped, True))

        return moves

    def get_all_moves(self, player):
        pieces = self.get_color_pieces(player)

        moves = {}
        for piece in pieces:
            move = self.valid_moves(piece)
            if move:
                moves[piece] = move

        return moves