import pygame as pg

from piece import Piece

pg.font.init()
font_arial = pg.font.SysFont("Arial", 20)


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
        self.states: list[list[list[pg.Rect]]] = []

        self.is_moving: bool = False
        self.selected_piece: Piece | None = None

        self.turn = "w"

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

    def undo(self):
        if len(self.states):

            last_state = self.states.pop()

            # Testing
            self.states.append(
                [
                    [self.matrix[row][col].getCurrPos() for row in range(self.rows)]
                    for col in range(self.cols)
                ]
            )

            curr_state = self.states.pop()

            print("\n\n\n")
            print(last_state)
            for row in range(self.rows):
                for col in range(self.cols):
                    self.matrix[row][col].setCurrPos(last_state[row][col])
                print()

            print("\n\n\n")

            s = []
            for row in range(self.rows):
                for col in range(self.cols):
                    if last_state[row][col] != curr_state[row][col]:
                        print("L: ", end="")
                        print(last_state[row][col])
                        print("C: ", end="")
                        print(curr_state[row][col])
                    else:
                        s.append("s")

            print(s.count("s"))

    def draw(self, surface):
        light_brown = (193, 135, 70)
        dark_brown = (63, 35, 20)
        colors = [dark_brown, light_brown]
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

    def show_poss_moves(self, surface: pg.Surface):
        border_size = 3

        for row in range(self.rows):
            for col in range(self.cols):
                pos = pg.Rect(
                    col * self.cell_size + border_size / 2,
                    row * self.cell_size + border_size / 2,
                    self.cell_size - border_size,
                    self.cell_size - border_size,
                )

                # Show turn / other info
                if self.matrix[row][col].getColor() == self.turn:
                    pg.draw.rect(surface, "green", pos, border_size)

                # Selected Border
                if self.matrix[row][col] == self.selected_piece:
                    pg.draw.rect(surface, "red", pos, border_size)

                    # Possible positions
                    for p in self.matrix[row][col].getPossMoves():
                        pg.draw.rect(surface, "blue", p, border_size)

    def select(self, pos):
        x: int = pos[0] // self.cell_size
        y: int = pos[1] // self.cell_size
        clicked_piece: Piece = self.matrix[y][x]

        print("BEFORE SAVE")
        print(self.states)

        # Save state before new move
        self.states.append(
            [
                [self.matrix[row][col].getCurrPos() for row in range(self.rows)]
                for col in range(self.cols)
            ]
        )

        print("AFTER SAVE")
        print(self.states)

        if (
            self.selected_piece == None
            and clicked_piece.getType() != "e"
            and clicked_piece.getColor() == self.turn
        ):
            self.selected_piece = clicked_piece
            self.selected_piece.updatePossMoves(self.matrix, x, y)
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

                    # Switch turns
                    self.turn = "b" if self.turn == "w" else "w"

                    # Save state again after new move
                    # NOTE: state is removed right after
                    self.states.append(
                        [
                            [
                                self.matrix[row][col].getCurrPos()
                                for row in range(self.rows)
                            ]
                            for col in range(self.cols)
                        ]
                    )

                # Remove last saved state if no move is made
                self.states.pop()

                print("AFTER SELECT")
                print(self.states)

                self.is_moving = False
            self.selected_piece = None
