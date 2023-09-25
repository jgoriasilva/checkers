import pygame
from .board import Board
from .piece import Piece
from .constants import WHITE, RED

class Game():

    def __init__(self, win):
        self.win = win
        self.board = Board()
    
    def update(self):
        self.board.draw_squares(self.win)
        self.board.draw_pieces(self.win)
        self.board.draw_valid_moves(self.win)

    def valid_moves(self, piece: Piece):
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

        if not 0 <= target_row <= 7 or not 0 <= target_col <= 7:
            if skipping:
                moves.update({(row, col): skipped})
            return moves

        target_piece = self.board.get_piece(target_row, target_col)

        if not skipping:
            if target_piece is None:
                moves.update({(target_row, target_col): skipped})
            elif target_piece.color != color:
                destination = self.board.get_piece(target_row+direction, target_col+side)
                if destination is not None:
                    return moves
                else:
                    new_skipped = skipped + [(target_row, target_col)]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, +1, moves, new_skipped, True))
        
        else:
            if target_piece is None:
                moves.update({(row, col): skipped})
            else:
                destination = self.board.get_piece(target_row+direction, target_col+side)
                if destination is not None:
                    return moves
                else:
                    new_skipped = skipped + [(target_row, target_col)]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, +1, moves, new_skipped, True))

        return moves

    def select_piece(self, row, col):
        return self.board.get_piece(row, col)