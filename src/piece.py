import pygame as pg


class Piece:
    def __init__(self, type: str = "e", color: str = ""):
        self.setName(type)
        self.setType(type)

        self.pos: pg.Rect = None
        self.can_attack: bool = False

        self.color: str = color
        self.setImage()

        self.poss_moves: list[pg.Rect] = []
        self.move_count: int = 0

        self.range: list[pg.Rect] = []
        self.king_area: list[pg.Rect] = []

    def copy(self) -> "Piece":
        copied_piece = Piece(self.type, self.color)
        copied_piece.setMoveCount(self.move_count)
        copied_piece.setPos(self.pos)
        return copied_piece

    def getType(self) -> str:
        return self.type

    def setType(self, type: str) -> None:
        self.type = type
        self.setName(type)
        if type == "e":
            self.setColor("")

    def getName(self) -> str:
        return self.name

    def setName(self, type: str) -> None:
        types: dict[str] = {
            "e": "empty",
            "p": "pawn",
            "b": "bishop",
            "n": "knight",
            "r": "rook",
            "q": "queen",
            "k": "king",
        }
        self.name = types[type]

    def getColor(self) -> str:
        return self.color

    def setColor(self, color: str) -> None:
        self.color = color

    def getImage(self) -> pg.Surface:
        if self.type == "e":
            return None
        return self.image

    def setImage(self, image: pg.Surface = None):
        self.image: pg.Surface | None = None
        if image:
            self.image = image
        elif self.type != "e":
            self.image = pg.image.load(rf"assets\{self.name}-{self.color}.png")

    def getPos(self) -> pg.Rect:
        return self.pos

    def setPos(self, pos: pg.Rect) -> None:
        self.pos = pos

    def getMoveCount(self) -> int:
        return self.move_count

    def setMoveCount(self, move_count: int):
        self.move_count = move_count

    def clearAllMoves(self):
        self.poss_moves = []

    def getPossMoves(self) -> list[pg.Rect]:
        return self.poss_moves

    def setPossMoves(self, new_poss_moves: list[pg.Rect]) -> None:
        self.poss_moves = new_poss_moves

    def getRange(self) -> list[pg.Rect]:
        return self.range

    def setRange(self, new_range: list[pg.Rect]) -> None:
        self.range = new_range

    def updatePossMoves(
        self,
        matrix: list[list["Piece"]],
        x: int,
        y: int,
        include_pawn_attack: bool = False,
    ) -> None:
        global other_color
        other_color = "b" if self.color == "w" else "w"

        self.poss_moves: list[pg.Rect] = []
        length: int = len(matrix) - 1

        # Pawns
        if self.type == "p":
            self.getPawnMoves(matrix, x, y, length, include_pawn_attack)

        # Rooks
        if self.type == "r":
            self.getRookMoves(matrix, x, y, length)
            self.getRookRange(matrix, x, y, length)

        # Bishops
        if self.type == "b":
            self.getBishopMoves(matrix, x, y, length)
            self.getBishopRange(matrix, x, y, length)

        # knights
        if self.type == "n":
            self.getKnightMoves(matrix, x, y, length)

        # Queens
        if self.type == "q":
            self.getQueenMoves(matrix, x, y, length)

        # Kings
        if self.type == "k":
            self.getKingMoves(matrix, x, y, length)
            self.updateKingArea(matrix, x, y, length)

    def getPawnMoves(
        self,
        matrix: list[list["Piece"]],
        x: int,
        y: int,
        length: int,
        include_attack: bool = False,
    ):
        up = y - 1
        down = y + 1
        left = x - 1
        right = x + 1

        if self.color == "w":
            # Attack
            if up >= 0 and left >= 0:
                cell = matrix[up][left]
                if include_attack:
                    if cell.getColor() != "w":
                        self.poss_moves.append(cell.getPos())
                else:
                    if cell.getType() != "e" and cell.getColor() != "w":
                        self.poss_moves.append(cell.getPos())
            if up >= 0 and right <= length:
                cell = matrix[up][right]
                if include_attack:
                    if cell.getColor() != "w":
                        self.poss_moves.append(cell.getPos())
                else:
                    if cell.getType() != "e" and cell.getColor() != "w":
                        self.poss_moves.append(cell.getPos())

            # Default
            if up >= 0:
                has_default: bool = False
                cell = matrix[up][x]
                if cell.getType() == "e":
                    self.poss_moves.append(cell.getPos())
                    has_default: bool = True

                # 2x Up
                if up - 1 >= 0:
                    cell = matrix[up - 1][x]
                    if has_default and self.move_count == 0 and cell.getType() == "e":
                        self.poss_moves.append(cell.getPos())

        elif self.color == "b":
            # Attack
            if down <= length and right <= length:
                cell = matrix[down][right]
                if include_attack:
                    if cell.getColor() != "b":
                        self.poss_moves.append(cell.getPos())
                else:
                    if cell.getType() != "e" and cell.getColor() != "b":
                        self.poss_moves.append(cell.getPos())
            if down <= length and left >= 0:
                cell = matrix[down][left]
                if include_attack:
                    if cell.getColor() != "b":
                        self.poss_moves.append(cell.getPos())
                else:
                    if cell.getType() != "e" and cell.getColor() != "b":
                        self.poss_moves.append(cell.getPos())

            # Default
            if down <= length:
                has_default: bool = False
                cell = matrix[down][x]
                if cell.getType() == "e":
                    self.poss_moves.append(cell.getPos())
                    has_default: bool = True

                # 2x Down
                if down + 1 <= length:
                    cell = matrix[down + 1][x]
                    if has_default and self.move_count == 0 and cell.getType() == "e":
                        self.poss_moves.append(cell.getPos())

    def getRookMoves(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        # Left starting from piece
        for i in range(1, length + 1):
            left_dex = x - i
            if left_dex >= 0:
                cell = matrix[y][left_dex]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

        # Right starting from piece
        for i in range(1, length + 1):
            right_dex = x + i
            if right_dex <= length:
                cell = matrix[y][right_dex]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

        # Up starting from piece
        for i in range(1, length + 1):
            up_dex = y - i
            if up_dex >= 0:
                cell = matrix[up_dex][x]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

        # Down starting from piece
        for i in range(1, length + 1):
            down_dex = y + i
            if down_dex <= length:
                cell = matrix[down_dex][x]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

    def getRookRange(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        # Left starting from piece
        for i in range(1, length + 1):
            left_dex = x - i
            if left_dex >= 0:
                cell = matrix[y][left_dex]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

        # Right starting from piece
        for i in range(1, length + 1):
            right_dex = x + i
            if right_dex <= length:
                cell = matrix[y][right_dex]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

        # Up starting from piece
        for i in range(1, length + 1):
            up_dex = y - i
            if up_dex >= 0:
                cell = matrix[up_dex][x]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

        # Down starting from piece
        for i in range(1, length + 1):
            down_dex = y + i
            if down_dex <= length:
                cell = matrix[down_dex][x]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

    def getBishopMoves(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        # Up Left starting from piece
        for i in range(1, length + 1):
            up_dex = y - i
            left_dex = x - i
            if up_dex >= 0 and left_dex >= 0:
                cell = matrix[up_dex][left_dex]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

        # Up Right starting from piece
        for i in range(1, length + 1):
            up_dex = y - i
            right_dex = x + i
            if up_dex >= 0 and right_dex <= length:
                cell = matrix[up_dex][right_dex]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

        # Down Left starting from piece
        for i in range(1, length + 1):
            down_dex = y + i
            left_dex = x - i
            if down_dex <= length and left_dex >= 0:
                cell = matrix[down_dex][left_dex]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

        # Down Right starting from piece
        for i in range(1, length + 1):
            down_dex = y + i
            right_dex = x + i
            if down_dex <= length and right_dex <= length:
                cell = matrix[down_dex][right_dex]
                if cell.getType() == "e":
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                elif cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())
                    break
                else:
                    break

    def getBishopRange(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        # Up Left starting from piece
        for i in range(1, length + 1):
            up_dex = y - i
            left_dex = x - i
            if up_dex >= 0 and left_dex >= 0:
                cell = matrix[up_dex][left_dex]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

        # Up Right starting from piece
        for i in range(1, length + 1):
            up_dex = y - i
            right_dex = x + i
            if up_dex >= 0 and right_dex <= length:
                cell = matrix[up_dex][right_dex]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

        # Down Left starting from piece
        for i in range(1, length + 1):
            down_dex = y + i
            left_dex = x - i
            if down_dex <= length and left_dex >= 0:
                cell = matrix[down_dex][left_dex]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

        # Down Right starting from piece
        for i in range(1, length + 1):
            down_dex = y + i
            right_dex = x + i
            if down_dex <= length and right_dex <= length:
                cell = matrix[down_dex][right_dex]
                if cell.getPos() not in self.range:
                    self.range.append(cell.getPos())

    def getKnightMoves(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        offsets = [
            [-2, -1],
            [-1, -2],
            [1, -2],
            [2, -1],
            [2, 1],
            [1, 2],
            [-1, 2],
            [-2, 1],
        ]

        for offset in offsets:
            y2 = y + offset[1]
            x2 = x + offset[0]

            if x2 >= 0 and y2 >= 0 and x2 <= length and y2 <= length:
                cell = matrix[y2][x2]
                if cell.getType() == "e" or cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())

    def getKingMoves(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        offsets = [
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
        ]

        for offset in offsets:
            y2 = y + offset[1]
            x2 = x + offset[0]

            if x2 >= 0 and y2 >= 0 and x2 <= length and y2 <= length:
                cell = matrix[y2][x2]
                if cell.getType() == "e" or cell.getColor() == other_color:
                    if cell.getPos() not in self.poss_moves:
                        self.poss_moves.append(cell.getPos())

    def getQueenMoves(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        self.getRookMoves(matrix, x, y, length)
        self.getBishopMoves(matrix, x, y, length)
        self.getKnightMoves(matrix, x, y, length)
        self.getKingMoves(matrix, x, y, length)

        self.getRookRange(matrix, x, y, length)
        self.getBishopRange(matrix, x, y, length)

    def updateKingArea(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        offsets = [
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
        ]

        for offset in offsets:
            y2 = y + offset[1]
            x2 = x + offset[0]

            if x2 >= 0 and y2 >= 0 and x2 <= length and y2 <= length:
                cell = matrix[y2][x2]
                if cell.getPos() not in self.king_area:
                    self.king_area.append(cell.getPos())

    def getKingArea(self) -> list[pg.Rect]:
        return self.king_area
