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
        self.in_stalemate: bool = False

        self.game_over: bool = False

        self.turn: str = "white"
        self.other_turn: str = "black"
        self.winner: str | None = None

        self.my_poss_moves: list[pg.Rect] = []
        self.op_poss_moves: list[pg.Rect] = []

        self.new_poss_moves: list[pg.Rect] = []

        self.setup()

    def setup(self):
        self.matrix = [
            [
                Piece("r", "black"),
                Piece("n", "black"),
                Piece("b", "black"),
                Piece("q", "black"),
                Piece("k", "black"),
                Piece("b", "black"),
                Piece("n", "black"),
                Piece("r", "black"),
            ],
            [
                Piece("p", "black"),
                Piece("p", "black"),
                Piece("p", "black"),
                Piece("p", "black"),
                Piece("p", "black"),
                Piece("p", "black"),
                Piece("p", "black"),
                Piece("p", "black"),
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
                Piece("p", "white"),
                Piece("p", "white"),
                Piece("p", "white"),
                Piece("p", "white"),
                Piece("p", "white"),
                Piece("p", "white"),
                Piece("p", "white"),
                Piece("p", "white"),
            ],
            [
                Piece("r", "white"),
                Piece("n", "white"),
                Piece("b", "white"),
                Piece("q", "white"),
                Piece("k", "white"),
                Piece("b", "white"),
                Piece("n", "white"),
                Piece("r", "white"),
            ],
        ]
        # Set the piece positions
        for row in range(self.rows):
            for col in range(self.cols):
                pos = pg.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                piece = self.matrix[row][col]
                piece.setPos(pos)

    def setup_test(self):
        self.matrix = [
            [
                Piece(),
                Piece(),
                Piece(),
                Piece(),
                Piece("k", "black"),
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
                Piece("k", "white"),
                Piece(),
                Piece(),
                Piece(),
            ],
        ]
        # Set the piece positions
        for row in range(self.rows):
            for col in range(self.cols):
                pos = pg.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                piece = self.matrix[row][col]
                piece.setPos(pos)

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
                    # print(
                    #     last_state[row][col].getType()
                    #     + last_state[row][col].getColor()
                    #     + str(last_state[row][col].getMoveCount()),
                    #     end=",",
                    # )
                    print(
                        last_state[row][col].getType()
                        + last_state[row][col].getColor(),
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
            self.switch_turns()

    def switch_turns(self):
        self.turn = "black" if self.turn == "white" else "white"
        self.other_turn = "black" if self.other_turn == "white" else "white"

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

                piece: Piece = self.matrix[row][col]

                # Checkerboard
                pg.draw.rect(surface, colors[int(color_type)], pos)

                # Chess Piece
                image: pg.Surface = piece.getImage()
                if image:
                    surface.blit(image, pos)

                # Switch for board coloring
                color_type = not color_type
            color_type = not color_type

        # Show Checkmate & Game Over
        padding: int = 50
        if self.in_checkmate:
            checkmate_surface: pg.Surface = font_arial.render(
                "  Checkmate!!!  ", True, "white", None
            )
            self.winner: str = "Black" if self.turn == "white" else "White"
            winner_surface: pg.Surface = font_arial.render(
                f"  {self.winner} Wins  ", True, "white", None
            )

            checkmate_rect: pg.Rect = checkmate_surface.get_rect()
            checkmate_rect.center = (self.width // 2, self.height // 2 - padding)
            winner_rect: pg.Rect = winner_surface.get_rect()
            winner_rect.center = (self.width // 2, self.height // 2 + padding)

            surface.blit(checkmate_surface, checkmate_rect)
            surface.blit(winner_surface, winner_rect)
        elif self.in_stalemate:
            game_over_surface: pg.SurfaceType = font_arial.render(
                " Stalemate!!! ", True, "white", None
            )
            game_over_rect: pg.Rect = game_over_surface.get_rect()
            game_over_rect.center = (self.width // 2, self.height // 2)

            surface.blit(game_over_surface, game_over_rect)
        elif self.game_over:
            game_over_surface: pg.SurfaceType = font_arial.render(
                " Game Over ", True, "white", None
            )
            game_over_rect: pg.Rect = game_over_surface.get_rect()
            game_over_rect.center = (self.width // 2, self.height // 2)

            surface.blit(game_over_surface, game_over_rect)

    def showPossMoves(self, surface: pg.Surface, debug: bool = False):
        if debug:
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
                    if len(self.my_poss_moves):
                        for move in self.my_poss_moves:
                            pg.draw.circle(
                                surface,
                                self.turn,
                                (move[0] + (move[2] / 2), move[1] + (move[3] / 2)),
                                move[2] / 4,
                                border_size,
                            )

                    if len(self.op_poss_moves):
                        for move in self.op_poss_moves:
                            pg.draw.rect(
                                surface,
                                self.other_turn,
                                pg.Rect(
                                    move[0] + move[2] / 4,
                                    move[1] + move[3] / 4,
                                    move[2] / 2,
                                    move[3] / 2,
                                ),
                                border_size,
                            )

    def updateAllPossMoves(self):
        self.my_poss_moves: list[pg.Rect] = []
        self.op_poss_moves: list[pg.Rect] = []

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.matrix[row][col]
                if piece.getPos():
                    x: int = piece.getPos()[0] // self.cell_size
                    y: int = piece.getPos()[1] // self.cell_size
                    if piece.getColor() == self.turn:
                        self.updateMyPossMoves(piece, x, y)
                    else:
                        self.updateOpPossMoves(piece, x, y)

        # print(f"{self.turn}'s poss moves")
        # print(self.my_poss_moves)
        # print()
        # print(f"{self.other_turn}'s poss moves")
        # print(self.op_poss_moves)

    def updateMyPossMoves(self, piece: Piece, x: int, y: int):
        piece.updatePossMoves(self.matrix, x, y)

        for move in piece.getPossMoves():
            if move not in self.my_poss_moves:
                self.my_poss_moves.append(move)

    def updateOpPossMoves(self, piece: Piece, x: int, y: int):
        piece.updatePossMoves(self.matrix, x, y)

        for move in piece.getPossMoves():
            if move not in self.op_poss_moves:
                self.op_poss_moves.append(move)

    def addOpPawnAttacks(self):
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.matrix[row][col]
                if (
                    piece.getPos()
                    and piece.getColor() == self.other_turn
                    and piece.getType() == "p"
                ):
                    x: int = piece.getPos()[0] // self.cell_size
                    y: int = piece.getPos()[1] // self.cell_size
                    for move in piece.getPawnMoves(
                        self.matrix, x, y, len(self.matrix) - 1, include_attack=True
                    ):
                        if move not in self.op_poss_moves:
                            self.op_poss_moves.append(move)

    # FIXME: Removes all Pawn moves (Should remove pawn Attack moves ONLY)
    def removeOpPawnAttacks(self):
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.matrix[row][col]
                if (
                    piece.getPos()
                    and piece.getColor() == self.other_turn
                    and piece.getType() == "p"
                ):
                    x: int = piece.getPos()[0] // self.cell_size
                    y: int = piece.getPos()[1] // self.cell_size
                    for move in piece.getPawnMoves(
                        self.matrix, x, y, len(self.matrix) - 1, include_attack=True
                    ):
                        if move in self.op_poss_moves:
                            self.op_poss_moves.remove(move)

    def checkInOtherPossMoves(self, pos: pg.Rect) -> list[bool, pg.Rect]:
        other_turn: str = "black" if self.turn == "white" else "white"

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
        other_turn: str = "black" if self.turn == "white" else "white"

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

    def getMyKing(self) -> Piece | None:
        """Get the current turn's King if it exists"""

        for row in range(self.rows):
            for col in range(self.cols):
                if (
                    self.matrix[row][col].getType() == "k"
                    and self.matrix[row][col].getColor() == self.turn
                ):
                    return self.matrix[row][col]
        return None

    def getOpKing(self) -> Piece | None:
        """Get the other turn's King if it exists"""

        for row in range(self.rows):
            for col in range(self.cols):
                if (
                    self.matrix[row][col].getType() == "k"
                    and self.matrix[row][col].getColor() == self.other_turn
                ):
                    return self.matrix[row][col]
        return None

    def isMyKingInCheck(self) -> bool:
        """Check if the current turn's king is in check
        and return True if it is"""

        for row in range(self.rows):
            for col in range(self.cols):
                other_piece = self.matrix[row][col]
                if other_piece.getColor() == self.other_turn:
                    if self.getMyKing().getPos() in other_piece.getPossMoves():
                        return True

        return False

    def isMyKingInCheckmate(self) -> bool:
        """Check if the current turn's King is in checkmate
        and set the class's in_checkmate variable to True if it is"""

        if self.in_check:
            if not len(self.getMyKing().getPossMoves()):
                return True

        return False

    def isStalemate(self) -> bool:
        all_pieces: list[Piece] = []
        piece_set: list[Piece] = []

        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.matrix[row][col]
                if piece.getType() == "k":
                    piece_set.append(piece)
                if piece.getType() != "e":
                    all_pieces.append(piece)

        return len(piece_set) == len(all_pieces)

    def tempMovePiece(self, temp_spot: Piece) -> tuple[str, str]:
        """Temporarily move selected_piece to one of its possible positions"""
        prev_temp_type, prev_temp_color = temp_spot.getType(), temp_spot.getColor()

        temp_spot.setType(self.selected_piece.getType())
        temp_spot.setColor(self.selected_piece.getColor())
        self.selected_piece.setType("e")

        self.updateAllPossMoves()
        self.addOpPawnAttacks()

        return (prev_temp_type, prev_temp_color)

    def returnTempMovedPiece(
        self,
        temp_spot: Piece,
        prev_type: str,
        prev_color: str,
        prev_temp_type: str,
        prev_temp_color: str,
    ) -> Piece:
        self.selected_piece.setType(prev_type)
        self.selected_piece.setColor(prev_color)

        temp_spot.setType(prev_temp_type)
        temp_spot.setColor(prev_temp_color)

        self.updateAllPossMoves()
        # self.removeOpPawnAttacks() # NOTE: Uncomment once method is fixed

        return temp_spot

    def tempRemovePiece(self):
        """Temporarily remove selected_piece from the board
        and see what the opponents possible moves will look like"""

        self.selected_piece.setType("e")

        self.updateAllPossMoves()
        self.addOpPawnAttacks()

    def returnTempRemovedPiece(self, prev_type: str, prev_color: str):
        self.selected_piece.setType(prev_type)
        self.selected_piece.setColor(prev_color)

        self.updateAllPossMoves()
        # self.removeOpPawnAttacks() # NOTE: Uncomment once method is fixed

    def removeMovesThatDontExitCheck(self, prev_type: str, prev_color: str):
        self.new_poss_moves = []
        current_poss_moves = self.selected_piece.getPossMoves()

        for move in current_poss_moves:
            temp_spot_x: int = move[0] // self.cell_size
            temp_spot_y: int = move[1] // self.cell_size
            temp_spot: Piece = self.matrix[temp_spot_y][temp_spot_x]

            prev_temp_type, prev_temp_color = self.tempMovePiece(temp_spot)

            # Check if the king is still in check after the pseudo move
            is_my_king_in_check = self.isMyKingInCheck()

            # move the selected_piece back to its original position
            self.matrix[temp_spot_y][temp_spot_x] = self.returnTempMovedPiece(
                temp_spot, prev_type, prev_color, prev_temp_type, prev_temp_color
            )

            if not is_my_king_in_check:
                self.new_poss_moves.append(move)

        # Remove move from overall possible moves
        for move in current_poss_moves:
            if move not in self.new_poss_moves:
                self.my_poss_moves.remove(move)

    def canMovePiece(self) -> bool:
        """Check if the selected_piece can move safely"""

        prev_type = self.selected_piece.getType()
        prev_color = self.selected_piece.getColor()

        # Check if the selected_piece can move to REMOVE king from check
        if self.in_check:
            self.removeMovesThatDontExitCheck(prev_type, prev_color)

            # If the array of moves is not empty then we can move out of check
            if len(self.new_poss_moves):
                return True
            else:
                return False

        # Check if the selected_piece can move without PUTTING king in check
        else:
            # If the selected_piece is the king,
            # then we need to remove its moves that will put it into check
            if self.selected_piece == self.getMyKing():
                self.removeMovesThatDontExitCheck(prev_type, prev_color)

                # If the array of moves is not empty then we can move without putting king in check
                if len(self.new_poss_moves):
                    self.selected_piece.setPossMoves(self.new_poss_moves)
                    return True
                else:
                    self.selected_piece.setPossMoves([])
                    return False
            else:
                self.tempRemovePiece()

                # Check if the current turn's King is now in check
                is_my_king_in_check = self.isMyKingInCheck()

                # Return the selected_piece back to the board
                self.returnTempRemovedPiece(prev_type, prev_color)

                if is_my_king_in_check:
                    # Therefore, the selected_piece CANNOT move
                    return False
                else:
                    # Therefore, the selected_piece CAN move
                    return True

    def select(self, pos: pg.Rect):
        x: int = pos[0] // self.cell_size
        y: int = pos[1] // self.cell_size
        clicked_piece: Piece = self.matrix[y][x]

        if (
            self.selected_piece == None
            and clicked_piece.getType() != "e"
            and clicked_piece.getColor() == self.turn
        ):
            self.updateAllPossMoves()

            self.selected_piece = clicked_piece

            if self.in_check:
                # Remove all moves that will keep the current turn's King in check
                if self.canMovePiece():
                    self.selected_piece.setPossMoves(self.new_poss_moves)
                    self.is_moving = True
                else:
                    # Remove all moves from the selected piece so it can not move
                    self.selected_piece.setPossMoves([])
                    self.is_moving = False
            else:
                # Check if the selected_piece can move without putting king in check
                if self.canMovePiece():
                    self.is_moving = True
                else:
                    self.is_moving = False
        else:
            if self.is_moving:
                if clicked_piece.getPos() in self.selected_piece.getPossMoves():
                    clicked_piece.setType(self.selected_piece.getType())
                    clicked_piece.setColor(self.selected_piece.getColor())
                    clicked_piece.setImage(self.selected_piece.getImage())
                    clicked_piece.setMoveCount(self.selected_piece.getMoveCount() + 1)

                    self.selected_piece.setType("e")
                    self.in_check = False

                    # Check if other turn's king just got captured
                    if not self.getOpKing():
                        self.game_over = True
                    else:
                        self.switch_turns()

                        self.updateAllPossMoves()

                        if self.isMyKingInCheck():
                            self.in_check = True

                        if self.isMyKingInCheckmate():
                            self.in_checkmate = True
                            self.game_over = True

                        if self.isStalemate():
                            self.in_stalemate = True
                            self.game_over = True
                else:
                    pass

                self.is_moving = False
            self.selected_piece = None
            self.updateAllPossMoves()

    # NOTE: Take save state code from here and move to new select method
    def select2(self, pos: pg.Rect):
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
                    # Pretend a piece moves into one of its possible possiitions.
                    # If that move happens and the king is still in check then we can't make that move.
                    # So then, delete that move from the selected piece's possible moves
                    self.RemoveMovesThatDontExitCheck()
                else:
                    self.updateAllPossMoves()

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

                    self.switch_turns()

                    self.checkForCheck()
                    self.checkForCheckMate()
                else:
                    # Remove last saved state if no move is made
                    self.states.pop()

                self.is_moving = False
            self.selected_piece = None
