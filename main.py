import pygame
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, RED, WHITE
from checkers.board import Board
from checkers.piece import Piece
from checkers.game import Game

FPS = 60

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.board.valid_moves = game.valid_moves(game.select_piece(row,col))
    
        game.update()
        pygame.display.update()
    
    pygame.quit()


main()