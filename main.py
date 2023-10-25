import pygame
from checkers.constants import *
from checkers.board import Board
from checkers.piece import Piece
from checkers.game import Game
import ai.minimax as ai

FPS = 60

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(win)

    while run:
        clock.tick(FPS)

        game_over, winner = game.is_game_over()
        if game_over:
            print(f"Game over. Winner: {winner}")
            run = False
            
        if game.turn == WHITE:
            score, board = ai.algorithm(game.board, player=WHITE, depth=2)
            game.board = board
            game.change_turn()

        # if game.turn == RED:
        #     score, board = ai.algorithm(game.board, player=RED, depth=6)
        #     game.board = board
        #     game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
    
        game.update()
        pygame.display.update()

    
    pygame.quit()

if __name__ == '__main__':
    main()