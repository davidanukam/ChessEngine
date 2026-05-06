import pygame as pg
import pywinstyles
import sys

from board import Board


def main():
    pg.init()

    WIDTH, HEIGHT = 768, 768
    FPS = 60

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chess")
    pywinstyles.change_header_color(screen, "black")

    icon = pg.image.load("../assets/board.png")
    pg.display.set_icon(icon)

    clock = pg.time.Clock()

    board = Board(WIDTH, HEIGHT)

    running: bool = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                board.select(event.pos)

        ## Update

        ## Draw
        screen.fill("black")

        board.draw(screen)
        board.show_poss_moves(screen)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
