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

        if skipping:
            moves.update({(row, col): skipped})
        if not 0 <= target_row <= 7 or not 0 <= target_col <= 7:
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
                    skipped_piece = self.board.get_piece(target_row, target_col)
                    new_skipped = skipped + [skipped_piece]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, +1, moves, new_skipped, True))
        
        else:
            if target_piece is None:
                moves.update({(row, col): skipped})
            elif target_piece.color != color:
                destination = self.board.get_piece(target_row+direction, target_col+side)
                if destination is not None:
                    return moves
                else:
                    skipped_piece = self.board.get_piece(target_row, target_col)
                    new_skipped = skipped + [skipped_piece]
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, -1, moves, new_skipped, True))
                    moves.update(self.__explore(target_row+direction, target_col+side, color, direction, +1, moves, new_skipped, True))

        return moves

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
                self.board.valid_moves = self.valid_moves(piece)


    def __move(self, target_row, target_col):
        
        target_move = (target_row, target_col)
        target = self.board.get_piece(target_row, target_col)
        if self.selected is not None and target is None and target_move in self.board.valid_moves:
            self.board.move_piece(self.selected, target_row, target_col)
            skipped = self.board.valid_moves[target_move]
            if len(skipped):
                self.board.remove_piece(skipped)
            self.change_turn()
            self.selected = None
        else:
            return False

        return True

    def is_game_over(self):
        if self.board.count[WHITE] <= 0:
            return True, "red"
        if self.board.count[RED] <= 0:
            return True, "white"

        return False, None

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