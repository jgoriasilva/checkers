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

RED_MOVE = pygame.USEREVENT + 1
RED_AI = 1
WHITE_MOVE = pygame.USEREVENT + 2
WHITE_AI = 0

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def check_game_over(game):
    game_over, winner = game.is_game_over()
    if game_over:
        print(f"Game over. Winner: {winner}")
    
    return game_over

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(win)

    while run:
        clock.tick(FPS)

        game.update()
        pygame.display.update()
            
        if game.turn==RED:
            pygame.event.post(pygame.event.Event(RED_MOVE))
        
        if game.turn == WHITE:
            pygame.event.post(pygame.event.Event(WHITE_MOVE))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == RED_MOVE:
                if RED_AI:
                    score, board = ai.algorithm(game.board, player=RED, depth=RED_AI)
                    game.board = board
                    game.change_turn()
                    run = not check_game_over(game)
                else:
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            run = False
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            break
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    if game.select(row, col):
                        run = not check_game_over(game)
            
            if event.type == WHITE_MOVE:
                if WHITE_AI:
                    score, board = ai.algorithm(game.board, player=WHITE, depth=WHITE_AI)
                    game.board = board
                    game.change_turn()
                    run = not check_game_over(game)
                else:
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            run = False
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            break
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    if game.select(row, col):
                        run = not check_game_over(game)

    pygame.quit()

if __name__ == '__main__':
    main()