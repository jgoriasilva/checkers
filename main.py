import pygame
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, RED, WHITE
from checkers.board import Board
from checkers.piece import Piece

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
    board = Board()
    board.create_pieces()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                piece = board.get_piece(row, col)
                board.move_piece(piece, 4, 3)
    
        board.draw_squares(win)
        board.draw_pieces(win)
        pygame.display.update()
    
    pygame.quit()


main()