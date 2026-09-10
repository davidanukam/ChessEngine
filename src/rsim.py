import pygame as pg
import pywinstyles
import sys

import random
import pyautogui

from src.board import Board


def rsim():
    global w_positions, w_poss_positions, b_positions, b_poss_positions

    pg.init()

    WIDTH, HEIGHT = 768, 768
    FPS = 60

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chess")
    pywinstyles.change_header_color(screen, "black")

    icon = pg.image.load("assets/board.png")
    pg.display.set_icon(icon)

    clock = pg.time.Clock()

    board = Board(WIDTH, HEIGHT)

    # w_positions: list[pg.Rect] = []
    # w_poss_positions: list[pg.Rect] = []

    # b_positions: list[pg.Rect] = []
    # b_poss_positions: list[pg.Rect] = []

    def update_poss():
        global w_positions, w_poss_positions, b_positions, b_poss_positions

        w_positions = []
        w_poss_positions = []
        b_positions = []
        b_poss_positions = []

        for row in range(len(board.matrix)):
            for col in range(len(board.matrix[0])):
                piece = board.matrix[row][col]
                if piece.getColor() == "w":
                    if piece.getPos() not in w_positions:
                        w_positions.append(piece.getPos())

                    for move in piece.getPossMoves():
                        if move not in w_poss_positions:
                            w_poss_positions.append(move)
                elif piece.getColor() == "b":
                    if piece.getPos() not in b_positions:
                        b_positions.append(piece.getPos())

                    for move in piece.getPossMoves():
                        if move not in b_poss_positions:
                            b_poss_positions.append(move)

    update_poss()

    timer = 1
    seconds_to_wait = 0.1

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
                update_poss()
                board.updateAllPossMoves()

                if board.selected_piece == None:
                    pos = None

                    if board.turn == "w":
                        movable_w_positions = []

                        for i in range(len(w_positions)):
                            if len(
                                board.matrix[w_positions[i][1] // board.cell_size][
                                    w_positions[i][0] // board.cell_size
                                ].getPossMoves()
                            ):
                                movable_w_positions.append(w_positions[i])

                        pos = random.choice(movable_w_positions)
                    else:
                        movable_b_positions = []

                        for j in range(len(b_positions)):
                            if len(
                                board.matrix[b_positions[j][1] // board.cell_size][
                                    b_positions[j][0] // board.cell_size
                                ].getPossMoves()
                            ):
                                movable_b_positions.append(b_positions[j])

                        pos = random.choice(movable_b_positions)

                    if pos:
                        board.select((pos[0], pos[1]))
                else:
                    if len(board.selected_piece.getPossMoves()):
                        pos = random.choice(board.selected_piece.getPossMoves())

                        board.select((pos[0], pos[1]))
                    else:
                        board.game_over = True

                # Take a screenshot before exiting if it errors
                screenshot = pyautogui.screenshot()

                screenshot.save("chess_screen.png")

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
