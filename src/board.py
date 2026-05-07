import pygame as pg

from piece import Piece


class Board:
    def __init__(self, width: int, height: int):
        self.types: dict[str] = {
            "e": "empty",
            "p": "pawn",
            "b": "bishop",
            "n": "knight",
            "r": "rook",
            "q": "queen",
            "k": "king",
        }
        self.width: int = width
        self.height: int = height
        self.cell_size: int = max(width, height) // 8
        self.rows: int = width // self.cell_size
        self.cols: int = height // self.cell_size
        self.matrix: list[list[Piece]] = [
            [Piece("e") for i in range(self.cols)] for j in range(self.rows)
        ]

        self.is_moving: bool = False
        self.selected_piece: Piece | None = None

        self.setup()

    def setup(self):
        self.matrix = [
            [
                Piece("r", "b"),
                Piece("n", "b"),
                Piece("b", "b"),
                Piece("q", "b"),
                Piece("k", "b"),
                Piece("b", "b"),
                Piece("n", "b"),
                Piece("r", "b"),
            ],
            [
                Piece("p", "b"),
                Piece("p", "b"),
                Piece("p", "b"),
                Piece("p", "b"),
                Piece("p", "b"),
                Piece("p", "b"),
                Piece("p", "b"),
                Piece("p", "b"),
            ],
            [
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
            ],
            [
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
            ],
            [
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
            ],
            [
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece(),
            ],
            [
                Piece("p", "w"),
                Piece("p", "w"),
                Piece("p", "w"),
                Piece("p", "w"),
                Piece("p", "w"),
                Piece("p", "w"),
                Piece("p", "w"),
                Piece("p", "w"),
            ],
            [
                Piece("r", "w"),
                Piece("n", "w"),
                Piece("b", "w"),
                Piece("q", "w"),
                Piece("k", "w"),
                Piece("b", "w"),
                Piece("n", "w"),
                Piece("r", "w"),
            ],
        ]

    def getTypes(self) -> dict[int]:
        return self.types

    def draw(self, surface):
        colors = ["white", "green"]
        color_type = False

        for row in range(self.rows):
            for col in range(self.cols):
                # Tile
                pos = pg.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                # Checkerboard
                pg.draw.rect(surface, colors[int(color_type)], pos)

                # Chess Piece
                image: pg.Surface = self.matrix[row][col].getImage()
                if image:
                    surface.blit(image, pos)

                # Set Og Position (for pawns first move)
                if self.matrix[row][col].getOgPos() == None:
                    self.matrix[row][col].setOgPos(pos)

                # Update the Curr Position of any piece
                if self.matrix[row][col].getCurrPos() != pos:
                    self.matrix[row][col].setCurrPos(pos)

                # Switch for board coloring
                color_type = not color_type
            color_type = not color_type

    def show_poss_moves(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                pos = pg.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                # Selected Border
                if self.matrix[row][col] == self.selected_piece:
                    pg.draw.rect(surface, "red", pos, 5)

                    # Possible positions
                    for p in self.matrix[row][col].getPossMoves():
                        pg.draw.rect(surface, "blue", p, 5)

    def select(self, pos):
        x: int = pos[0] // self.cell_size
        y: int = pos[1] // self.cell_size
        clicked_piece: Piece = self.matrix[y][x]
        if self.selected_piece == None and clicked_piece.getType() != "e":
            self.selected_piece = clicked_piece
            self.selected_piece.updatePossMoves(self.matrix, x, y, self.cell_size)
            self.is_moving = True
        else:
            if self.is_moving:
                moving_piece_row: int = (
                    self.selected_piece.getCurrPos()[1] // self.cell_size
                )
                moving_piece_col: int = (
                    self.selected_piece.getCurrPos()[0] // self.cell_size
                )
                moving_piece: Piece = self.matrix[moving_piece_row][moving_piece_col]

                if clicked_piece.getCurrPos() in moving_piece.getPossMoves():
                    clicked_piece.setType(moving_piece.getType())
                    clicked_piece.setColor(moving_piece.getColor())
                    clicked_piece.setImage(moving_piece.getImage())
                    clicked_piece.setMoveCount(moving_piece.getMoveCount() + 1)

                    moving_piece.setType("e")

                self.is_moving = False
            self.selected_piece = None
