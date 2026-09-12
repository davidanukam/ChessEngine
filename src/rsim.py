import pygame as pg
import pywinstyles
import sys

import random

from src.board import Board


def rsim():
    global w_positions, w_poss_positions, b_positions, b_poss_positions

    pg.init()

    WIDTH, HEIGHT = 768, 768
    FPS = 60

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chess Sim")
    pywinstyles.change_header_color(screen, "black")

    icon = pg.image.load("assets/board.png")
    pg.display.set_icon(icon)

    clock = pg.time.Clock()

    board = Board(WIDTH, HEIGHT)

    w_positions = []
    w_poss_positions = []
    b_positions = []
    b_poss_positions = []

    def update_poss():
        global w_positions, w_poss_positions, b_positions, b_poss_positions

        w_positions = []
        w_poss_positions = []
        b_positions = []
        b_poss_positions = []

        for row in range(len(board.matrix)):
            for col in range(len(board.matrix[0])):
                piece = board.matrix[row][col]
                if piece.getColor() == "white":
                    if piece.getPos() not in w_positions:
                        w_positions.append(piece.getPos())

                    for move in piece.getPossMoves():
                        if move not in w_poss_positions:
                            w_poss_positions.append(move)
                elif piece.getColor() == "black":
                    if piece.getPos() not in b_positions:
                        b_positions.append(piece.getPos())

                    for move in piece.getPossMoves():
                        if move not in b_poss_positions:
                            b_poss_positions.append(move)

    board.updateAllPossMoves()
    update_poss()

    timer = 1
    seconds_to_wait = 0.25

    running: bool = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if not board.game_over:
                    board.select(event.pos)
            if event.type == pg.KEYDOWN:
                if not board.game_over:
                    if event.key == pg.K_z:
                        board.undo()
                    if event.key == pg.K_h:
                        board.help("Last State")
                    if event.key == pg.K_p:
                        board.print("Curr State")

        if timer % (FPS * seconds_to_wait) == 0:
            if not board.game_over:

                if board.selected_piece == None:
                    board.updateAllPossMoves()
                    update_poss()
                    if board.turn == "white":
                        while len(w_positions):
                            # Click one white piece at random
                            random_move = random.choice(w_positions)

                            board.select(random_move)

                            poss_moves = board.selected_piece.getPossMoves()
                            if not len(poss_moves):
                                w_positions.remove(random_move)
                                board.selected_piece = None
                            else:
                                break

                        if not len(w_positions):
                            board.game_over = True
                    else:
                        while len(b_positions):
                            # Click one black piece at random
                            random_move = random.choice(b_positions)

                            board.select(random_move)

                            poss_moves = board.selected_piece.getPossMoves()
                            if not len(poss_moves):
                                b_positions.remove(random_move)
                                board.selected_piece = None
                            else:
                                break

                        if not len(b_positions):
                            board.game_over = True
                else:
                    poss_moves = board.selected_piece.getPossMoves()
                    random_poss_move = random.choice(poss_moves)

                    board.select(random_poss_move)

        ## Draw
        screen.fill("black")

        board.draw(screen)
        if not board.game_over:
            board.showPossMoves(screen)

        timer += 1

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
    sys.exit()
