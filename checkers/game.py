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
        row, col, color = piece.row, piece.col, piece.color

        moves.update(self.__explore(row, col, color, -1, moves, []))
        moves.update(self.__explore(row, col, color, +1, moves, []))

        return moves

    def __explore(self, row, col, color, side, moves, skipped, skipping=False):
        direction = 1 if color == WHITE else -1
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
                    moves.update(self.__explore(target_row+direction, target_col+side, color, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, +1, moves, new_skipped, True))
        
        else:
            if target_piece is None:
                moves.update({(row, col): skipped})
            else:
                destination = self.board.get_piece(target_row+direction, target_col+side)
                if destination is not None:
                    return moves
                else:
                    new_skipped = skipped + [(target_row, target_col)]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, +1, moves, new_skipped, True))




        # if skipping:
        #     if target_piece == None:
        #         moves.update({(row,col):skipped})
        #     elif target_piece.color != color:
        #         destination = self.board.get_piece(target_row+direction, target_col+side)
        #         if destination == None:
        #             skipped.append(target_piece)
        #             moves.update(self.__explore(target_row+direction, target_col+side, color, side, moves, skipped, True))
        #         else:
        #             pass

        # else:
        #     if target_piece == None:
        #         moves.update({(target_row, target_col): skipped})
        #     elif target_piece.color != color:
        #         destination = self.board.get_piece(target_row+direction, target_col+side)
        #         if destination == None:
        #             moves.update({(row,col):skipped})
        #             skipped.append(target_piece)
        #             moves.update(self.__explore(target_row+direction, target_col-1, color, side, moves, skipped, True))
        #             moves.update(self.__explore(target_row+direction, target_col+1, color, side, moves, skipped, True))
        #         else:
        #             pass

        return moves

    def select_piece(self, row, col):
        return self.board.get_piece(row, col)