import pygame
from checkers.constants import WIDTH, HEIGHT, RED, WHITE
from checkers.board import Board
from checkers.piece import Piece

FPS = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    board.create_pieces()

    piece = board.get_piece(0,1)
    board.move_piece(piece, 4, 3)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        board.draw_squares(win)
        board.draw_pieces(win)
        pygame.display.update()
    
    pygame.quit()


main()