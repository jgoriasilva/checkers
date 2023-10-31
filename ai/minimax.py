'''
Idea:

- Get a board (root)

- Get all movements that are possible from root

- Simulate each movement

- Get resulting board (child)

- Get all movements

- Simulate each movement

- Repeat until max depth

- Evaluate score

- Return best move for player (either min or max)



#TODO: problem with valid_moves, solution is to probably add a filter at the end of get_valid_moves to filter moves to outside the board
#TODO: but the best solution would be to fix why these moves are being passed to the algorithm anyway

'''

from copy import deepcopy
from queue import SimpleQueue
from checkers.game import Game
from checkers.board import Board
from checkers.piece import Piece
from checkers.constants import WHITE, RED, shuffle_dict

def simulate(board: Board, piece, move):

    simulate_board = deepcopy(board)
    target_row, target_col = move

    simulate_piece = simulate_board.get_piece(piece.row, piece.col)
    valid_move = simulate_board.get_valid_moves(simulate_piece)
    skipped = valid_move[move]

    if move in valid_move:
        simulate_board.move_piece(simulate_piece, target_row, target_col, skipped)
    else:
        return None

    return simulate_board

def is_best_score(score, best_score, player):

    if player == WHITE: # max
        return score > best_score
    else: # min
        return score < best_score

def algorithm(board: Board, alpha=float('-inf'), beta=float('inf'), player=WHITE, depth=4):
    if depth == 0 or board.is_board_over()[0]:
        return board.evaluate(), board

    if player == WHITE: # max
        moves_dict = board.get_all_moves(player)
        moves_dict = shuffle_dict(moves_dict)

        best_score = float('-inf')

        if len(moves_dict) == 0:
            return best_score, board

        for piece in moves_dict:
            for move in moves_dict[piece]:
                simulate_board = simulate(board, piece, move)
                score, _ = algorithm(simulate_board, alpha, beta, RED, depth-1)
                if score > best_score:
                    best_board = simulate_board
                    best_score = score
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        

        return best_score, best_board

    else: # min
        moves_dict = board.get_all_moves(player)
        moves_dict = shuffle_dict(moves_dict)

        best_score = float('inf')

        if len(moves_dict) == 0:
            return best_score, board

        for piece in moves_dict:
            for move in moves_dict[piece]:
                simulate_board = simulate(board, piece, move)
                score, _ = algorithm(simulate_board, alpha, beta, WHITE, depth-1)
                if score < best_score:
                    best_board = simulate_board
                    best_score = score
                beta = min(beta, score)
                if beta <= alpha:
                    break
        
        return best_score, best_board