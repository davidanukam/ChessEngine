import pygame as pg

from src.piece import Piece

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

        self.op_poss_moves: list[pg.Rect] = []

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
        padding: int = 50
        if self.in_checkmate:
            self.game_over = True

            checkmate_surface: pg.Surface = font_arial.render(
                "  Checkmate!!!  ", True, "white", "black"
            )
            self.winner: str = "Black" if self.turn == "w" else "White"
            winner_surface: pg.Surface = font_arial.render(
                f"  {self.winner} Wins  ", True, "white", "black"
            )

            checkmate_rect: pg.Rect = checkmate_surface.get_rect()
            checkmate_rect.center = (self.width // 2, self.height // 2 - padding)
            winner_rect: pg.Rect = winner_surface.get_rect()
            winner_rect.center = (self.width // 2, self.height // 2 + padding)

            surface.blit(checkmate_surface, checkmate_rect)
            surface.blit(winner_surface, winner_rect)

        elif self.game_over:
            game_over_surface: pg.SurfaceType = font_arial.render(
                " Game Over ", True, "white", "black"
            )
            game_over_rect: pg.Rect = game_over_surface.get_rect()
            game_over_rect.center = (self.width // 2, self.height // 2)

            surface.blit(game_over_surface, game_over_rect)

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
                    pg.draw.rect(surface, "green", pos, border_size)
                    if self.matrix[row][col].getType() == "k":
                        pg.draw.rect(surface, "red", pos, border_size)
                # Show turn
                elif (
                    not self.in_checkmate
                    and self.matrix[row][col].getColor() == self.turn
                ):
                    pg.draw.rect(surface, "green", pos, border_size)

                # Selected Border
                if self.matrix[row][col] == self.selected_piece:
                    pg.draw.rect(surface, "white", pos, border_size)

                    # Possible positions
                    for p in self.matrix[row][col].getPossMoves():
                        p = pg.Rect(
                            p[0] + border_size / 2,
                            p[1] + border_size / 2,
                            p[2] - border_size,
                            p[3] - border_size,
                        )
                        pg.draw.rect(surface, "blue", p, border_size)

                # NOTE: Show all possible moves that the opponent can make
                # if len(self.op_poss_moves):
                #     for move in self.op_poss_moves:
                #         pg.draw.rect(
                #             surface,
                #             "purple",
                #             pg.Rect(
                #                 move[0] + move[2] / 4,
                #                 move[1] + move[3] / 4,
                #                 move[2] / 2,
                #                 move[3] / 2,
                #             ),
                #             border_size,
                #         )

    def updateAllPossMoves(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row][col].getPos():
                    x: int = self.matrix[row][col].getPos()[0] // self.cell_size
                    y: int = self.matrix[row][col].getPos()[1] // self.cell_size
                    self.matrix[row][col].updatePossMoves(self.matrix, x, y)

    def updateOpPossMoves(self):
        other_turn: str = "b" if self.turn == "w" else "w"

        for row in range(self.rows):
            for col in range(self.cols):
                if (
                    self.matrix[row][col].getPos()
                    and self.matrix[row][col].getColor() == other_turn
                ):
                    x: int = self.matrix[row][col].getPos()[0] // self.cell_size
                    y: int = self.matrix[row][col].getPos()[1] // self.cell_size
                    self.matrix[row][col].updatePossMoves(self.matrix, x, y, True)

    def checkInOtherPossMoves(self, pos: pg.Rect) -> list[bool, pg.Rect]:
        other_turn: str = "b" if self.turn == "w" else "w"

        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row][col].getColor() == other_turn:
                    other_poss_moves = self.matrix[row][col].getPossMoves()
                    for other_move in other_poss_moves:
                        if (
                            pos[0] == other_move[0]
                            and pos[1] == other_move[1]
                            and pos[2] == other_move[2]
                            and pos[3] == other_move[3]
                        ):
                            return [True, self.matrix[row][col].getPos()]
        return [False, None]

    def checkInOtherRanges(self, pos: pg.Rect) -> list[bool, pg.Rect]:
        other_turn: str = "b" if self.turn == "w" else "w"

        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row][col].getColor() == other_turn:
                    other_range = self.matrix[row][col].getRange()
                    for other_move in other_range:
                        if (
                            pos[0] == other_move[0]
                            and pos[1] == other_move[1]
                            and pos[2] == other_move[2]
                            and pos[3] == other_move[3]
                        ):
                            return [True, self.matrix[row][col].getPos()]
        return [False, None]

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
        other_turn: str = "b" if self.turn == "w" else "w"

        if not self.getKing():
            self.game_over = True
            return

        for row in range(self.rows):
            for col in range(self.cols):
                other_piece = self.matrix[row][col]
                if other_piece.getColor() == other_turn:
                    if self.getKing().getPos() in other_piece.getPossMoves():
                        self.in_check = True
                        return

    def checkForCheckMate(self):
        if self.in_check:
            if not len(self.getKing().getPossMoves()):
                self.in_checkmate = True
                self.in_check = False

    def checkIfMoveIntoCheck(self) -> bool:
        other_turn: str = "b" if self.turn == "w" else "w"
        self.op_poss_moves: list[pg.Rect] = []

        # Temporarily remove the selected piece from the board
        # And see if any opponent piece can now capture the king
        prev_type = self.selected_piece.getType()
        prev_color = self.selected_piece.getColor()
        self.selected_piece.setType("e")
        self.updateOpPossMoves()

        # Get all of the opponents possible moves (if the selected piece did not exist)
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.matrix[row][col]
                if piece.getColor() == other_turn:
                    for move in piece.getPossMoves():
                        if move not in self.op_poss_moves:
                            self.op_poss_moves.append(move)

        # Return selected piece back to where it was
        self.selected_piece.setType(prev_type)
        self.selected_piece.setColor(prev_color)
        self.updateOpPossMoves()

        if self.getKing():
            return self.getKing().getPos() in self.op_poss_moves
        return None

    def RemoveMovesThatDontExitCheck(self):
        prev_color = self.selected_piece.getColor()
        prev_type = self.selected_piece.getType()

        new_poss_moves: list[pg.Rect] = []

        # Check if the selected pieces possible moves will get the king out of check
        for move in self.selected_piece.getPossMoves():
            # Temporarily remove the selected piece from the board
            # And see if any opponent piece can now capture the king
            self.selected_piece.setType("e")

            row, col = move[1] // self.cell_size, move[0] // self.cell_size

            prev_move_type = self.matrix[row][col].getType()
            prev_move_color = self.matrix[row][col].getColor()

            self.matrix[row][col].setType(prev_type)
            self.matrix[row][col].setColor(prev_color)

            # Call this to update the self.op_poss_moves array
            self.checkIfMoveIntoCheck()

            # Check if the King is not in check after the pseudo move
            if self.getKing():
                if not self.getKing().getPos() in self.op_poss_moves:
                    new_poss_moves.append(move)
            else:
                return

            # Return pseudo move cell data back to what is was
            self.matrix[row][col].setType(prev_move_type)
            self.matrix[row][col].setColor(prev_move_color)

            # Return selected piece back to where it was
            self.selected_piece.setType(prev_type)
            self.selected_piece.setColor(prev_color)

            # Call this to update the self.op_poss_moves array
            self.checkIfMoveIntoCheck()

        self.selected_piece.setPossMoves(new_poss_moves)

        # For Pawns only:
        # If the 2x move remains but the 1x move doesn't
        # (meaning the pawn hasn't moved yet)
        # then remove both moves
        if self.selected_piece.getType() == "p":
            if len(self.selected_piece.getPossMoves()) == 1:
                # Check 2 cells above and 2 cells bellow
                if (
                    self.selected_piece.getPossMoves()[0][1] // self.cell_size
                    == (self.selected_piece.getPos()[1] // self.cell_size) + 2
                    or self.selected_piece.getPossMoves()[0][1] // self.cell_size
                    == (self.selected_piece.getPos()[1] // self.cell_size) - 2
                ):
                    self.selected_piece.setPossMoves([])

    def select(self, pos):
        x: int = pos[0] // self.cell_size
        y: int = pos[1] // self.cell_size
        clicked_piece: Piece = self.matrix[y][x]

        if (
            self.selected_piece == None
            and clicked_piece.getType() != "e"
            and clicked_piece.getColor() == self.turn
        ):
            # Update every piece's possible positions before we make any checks
            self.updateAllPossMoves()

            self.selected_piece = clicked_piece

            if self.in_checkmate:
                self.selected_piece = None
            else:
                self.is_moving = True

                # FIXME: Solve King Stalemate
                # Check stalemate
                if self.in_check:
                    pass


                # Pretend a piece moves into one of its possible possiitions.
                # If that move happens and the king is still in check then we can't make that move.
                # So then, delete that move from the selected piece's possible moves
                self.RemoveMovesThatDontExitCheck()

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
                    self.updateOpPossMoves()

                    # Switch turns
                    self.turn: str = "b" if self.turn == "w" else "w"
                    self.checkForCheck()
                    self.checkForCheckMate()
                else:
                    # Remove last saved state if no move is made
                    self.states.pop()

                self.is_moving = False
            self.selected_piece = None
