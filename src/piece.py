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

    def copy(self) -> "Piece":
        copied_pieve = Piece(self.type, self.color)
        copied_pieve.setMoveCount(self.move_count)
        copied_pieve.setPos(self.pos)
        return copied_pieve

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
            self.image = pg.image.load(rf"..\assets\{self.name}-{self.color}.png")

    def getPos(self) -> pg.Rect:
        return self.pos

    def setPos(self, pos: pg.Rect) -> None:
        self.pos = pos

    def getMoveCount(self) -> int:
        return self.move_count

    def setMoveCount(self, move_count: int):
        self.move_count = move_count

    def updatePossMoves(self, matrix: list[list["Piece"]], x: int, y: int) -> None:
        global other_color
        other_color = "b" if self.color == "w" else "w"

        self.poss_moves = []
        length = len(matrix) - 1

        # Pawns
        if self.type == "p":
            self.getPawnMoves(matrix, x, y, length)

        # Rooks
        if self.type == "r":
            self.getRookMoves(matrix, x, y, length)

        # Bishops
        if self.type == "b":
            self.getBishopMoves(matrix, x, y, length)

        # knights
        if self.type == "n":
            self.getKnightMoves(matrix, x, y, length)

        # Queens
        if self.type == "q":
            self.getQueenMoves(matrix, x, y, length)

        # Kings
        if self.type == "k":
            self.getKingMoves(matrix, x, y, length)

    def getPossMoves(self) -> list[pg.Rect]:
        return self.poss_moves

    def getPawnMoves(self, matrix: list[list["Piece"]], x: int, y: int, length: int):
        up = y - 1
        down = y + 1
        left = x - 1
        right = x + 1

        if self.color == "w":
            # Attack
            if up >= 0 and left >= 0:
                cell = matrix[up][left]
                if cell.getType() != "e" and cell.getColor() != "w":
                    self.poss_moves.append(cell.getPos())
            if up >= 0 and right <= length:
                cell = matrix[up][right]
                if cell.getType() != "e" and cell.getColor() != "w":
                    self.poss_moves.append(cell.getPos())

            # 2x Up
            cell = matrix[up][x]
            if self.move_count == 0 and cell.getType() == "e":
                self.poss_moves.append(matrix[up - 1][x].getPos())

            # Default
            if cell.getType() == "e":
                self.poss_moves.append(cell.getPos())

        elif self.color == "b":
            # Attack
            if down <= length and right <= length:
                cell = matrix[down][right]
                if cell.getType() != "e" and cell.getColor() != "b":
                    self.poss_moves.append(cell.getPos())
            if down <= length and left >= 0:
                cell = matrix[down][left]
                if cell.getType() != "e" and cell.getColor() != "b":
                    self.poss_moves.append(cell.getPos())

            # 2x Down
            cell = matrix[down][x]
            if self.move_count == 0 and cell.getType() == "e":
                self.poss_moves.append(matrix[down + 1][x].getPos())

            # Default
            if cell.getType() == "e":
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
