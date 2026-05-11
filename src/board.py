import pygame as pg

from piece import Piece

pg.font.init()
font_arial = pg.font.SysFont("Arial", 100, True)


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

        self.selected_piece: Piece | None = None
        self.states: list[list[list[Piece]]] = []

        self.is_moving: bool = False
        self.in_check: bool = False
        self.in_checkmate: bool = False
        self.game_over: bool = False

        self.turn: str = "w"
        self.winner: str | None = None

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

    def print(self, t: str):
        curr_state = self.matrix
        print(t)
        for row in range(self.rows):
            for col in range(self.cols):
                if curr_state[row][col].getType() == "e":
                    print(
                        curr_state[row][col].getType()
                        + "e"
                        + str(curr_state[row][col].getMoveCount()),
                        end=",",
                    )
                else:
                    print(
                        curr_state[row][col].getType()
                        + curr_state[row][col].getColor()
                        + str(curr_state[row][col].getMoveCount()),
                        end=",",
                    )
            print()
        print()

    def help(self, t: str):
        if len(self.states):
            last_state = self.states[-1]
            print(t)
            for row in range(self.rows):
                for col in range(self.cols):
                    print(
                        last_state[row][col].getType()
                        + last_state[row][col].getColor()
                        + str(last_state[row][col].getMoveCount()),
                        end=",",
                    )
                print()
            print()
        else:
            print("[]")

    def undo(self):
        if len(self.states):
            # Undo moves
            last_state = self.states.pop()

            for row in range(self.rows):
                for col in range(self.cols):
                    self.matrix[row][col] = last_state[row][col]
                    self.matrix[row][col].setMoveCount(
                        last_state[row][col].getMoveCount()
                    )

            # Unto turns
            self.turn = "b" if self.turn == "w" else "w"

    def update(self):
        # Update the possible moves of all pieces
        self.updateAllPossMoves()

        # Remove the positions that will keep king in check
        if self.in_check:
            self.removeCheckPossMoves()

        self.checkForCheckMate()

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

                chess_piece: Piece = self.matrix[row][col]

                # Checkerboard
                pg.draw.rect(surface, colors[int(color_type)], pos)

                # Chess Piece
                image: pg.Surface = chess_piece.getImage()
                if image:
                    surface.blit(image, pos)

                # Update the Position of all pieces
                if chess_piece.getPos() != pos:
                    chess_piece.setPos(pos)

                # Switch for board coloring
                color_type = not color_type
            color_type = not color_type

        # Show Checkmate & Game Over
        if self.in_checkmate:
            game_over_surface: pg.Surface = font_arial.render(
                "  GAME OVER!!!  ", True, "white", "black"
            )
            self.winner: str = "Black" if self.turn == "w" else "White"
            winner_surface: pg.Surface = font_arial.render(
                f"  {self.winner} Wins  ", True, "white", "black"
            )

            padding: int = 50
            game_over_rect: pg.Rect = game_over_surface.get_rect()
            game_over_rect.center = (self.width // 2, self.height // 2 - padding)
            winner_rect: pg.Rect = winner_surface.get_rect()
            winner_rect.center = (self.width // 2, self.height // 2 + padding)

            surface.blit(game_over_surface, game_over_rect)
            surface.blit(winner_surface, winner_rect)

    def showPossMoves(self, surface: pg.Surface):
        border_size = 3

        for row in range(self.rows):
            for col in range(self.cols):
                pos = pg.Rect(
                    col * self.cell_size + border_size / 2,
                    row * self.cell_size + border_size / 2,
                    self.cell_size - border_size,
                    self.cell_size - border_size,
                )

                # Show if in_check
                if self.in_check and self.matrix[row][col].getColor() == self.turn:
                    if self.matrix[row][col].getType() == "k":
                        pg.draw.rect(surface, "red", pos, border_size)
                # Show turn
                elif not self.in_checkmate and self.matrix[row][col].getColor() == self.turn:
                    pg.draw.rect(surface, "green", pos, border_size)

                # Selected Border
                if self.matrix[row][col] == self.selected_piece:
                    pg.draw.rect(surface, "white", pos, border_size)

                    # Possible positions
                    for p in self.matrix[row][col].getPossMoves():
                        pg.draw.rect(surface, "blue", p, border_size)

    def updateAllPossMoves(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # if self.matrix[row][col].getColor() == self.turn:
                if self.matrix[row][col].getPos():
                    x: int = self.matrix[row][col].getPos()[0] // self.cell_size
                    y: int = self.matrix[row][col].getPos()[1] // self.cell_size
                    self.matrix[row][col].updatePossMoves(self.matrix, x, y)

    def removeCheckPossMoves(self):
        for row in range(self.rows):
            for col in range(self.cols):
                curr_poss_moves: list[pg.Rect] = self.getKing().getPossMoves()
                other_poss_moves: list[pg.Rect] = self.matrix[row][col].getPossMoves()
                temp_poss_moves: list[pg.Rect] = []
                for poss_move in curr_poss_moves:
                    if poss_move not in other_poss_moves:
                        temp_poss_moves.append(poss_move)
                self.getKing().setPossMoves(temp_poss_moves)

    def getKing(self) -> Piece:
        for row in range(self.rows):
            for col in range(self.cols):
                if (
                    self.matrix[row][col].getType() == "k"
                    and self.matrix[row][col].getColor() == self.turn
                ):
                    return self.matrix[row][col]
        return None

    def checkForCheck(self):
        other_turn = "b" if self.turn == "w" else "w"

        for row in range(self.rows):
            for col in range(self.cols):
                other_piece = self.matrix[row][col]
                if other_piece.getColor() == other_turn:
                    if not self.getKing():
                        self.game_over = True
                        return
                    if self.getKing().getPos() in other_piece.getPossMoves():
                        self.in_check = True
                        break
            if self.in_check:
                break

    def checkForCheckMate(self):
        if self.in_check:
            if not len(self.getKing().getPossMoves()):
                self.in_checkmate = True
                self.in_check = False

    def select(self, pos):
        x: int = pos[0] // self.cell_size
        y: int = pos[1] // self.cell_size
        clicked_piece: Piece = self.matrix[y][x]

        if (
            self.selected_piece == None
            and clicked_piece.getType() != "e"
            and clicked_piece.getColor() == self.turn
        ):
            if self.in_check and clicked_piece.getType() != "k":
                self.selected_piece = None
            else:
                self.selected_piece = clicked_piece

                if self.in_checkmate:
                    self.selected_piece = None
                else:
                    self.is_moving = True

                    # Save state before new move
                    self.states.append(
                        [
                            [self.matrix[row][col].copy() for col in range(self.cols)]
                            for row in range(self.rows)
                        ]
                    )
        else:
            if self.is_moving:
                moving_piece_row: int = (
                    self.selected_piece.getPos()[1] // self.cell_size
                )
                moving_piece_col: int = (
                    self.selected_piece.getPos()[0] // self.cell_size
                )
                moving_piece: Piece = self.matrix[moving_piece_row][moving_piece_col]

                if clicked_piece.getPos() in moving_piece.getPossMoves():
                    clicked_piece.setType(moving_piece.getType())
                    clicked_piece.setColor(moving_piece.getColor())
                    clicked_piece.setImage(moving_piece.getImage())
                    clicked_piece.setMoveCount(moving_piece.getMoveCount() + 1)

                    moving_piece.setType("e")

                    self.in_check = False

                    self.updateAllPossMoves()

                    # Switch turns
                    self.turn = "b" if self.turn == "w" else "w"
                    self.checkForCheck()
                else:
                    # Remove last saved state if no move is made
                    self.states.pop()

                self.is_moving = False
            self.selected_piece = None
