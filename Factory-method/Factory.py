#!/usr/bin/env python3

import sys
import io
import os
import tempfile
import itertools
import unicodedata


DRAUGHT, PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN = ("DRAUGHT", "PAWN",
        "ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN")
BLACK, WHITE = ("BLACK", "WHITE")

if sys.platform.startswith("win"):
    def console(char, background):
        return char or " "
    sys.stdout = io.StringIO()
else:
    def console(char, background):
        return "\x1B[{}m{}\x1B[0m".format(43 if background == BLACK else 47, char or " ")


def make_new_method(char): # Needed to create a fresh method each time
    def new(Class): # Can't use super() or super(Piece, Class)
        return Piece.__new__(Class, char)
    return new


def main():
    checker = CheckersBoard()
    print(checker)

    chess = ChessBoard()
    print(chess)
    if sys.platform.startswith("win"):
        filename = os.path.join(tempfile.gettempdir(), "gameboard.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(sys.stdout.getvalue())
        print("wrote '{}'".format(filename), file=sys.__stdout__)


class Piece(str):

    __slots__ = ()


for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    char = chr(code)
    name = unicodedata.name(char).title().replace(" ", "")
    if name.endswith("sMan"):
        name = name[:-4]
    new = (lambda char: lambda Class: Piece.__new__(Class, char))(char)
    new.__name__ = "__new__"
    Class = type(name, (Piece,), dict(__slots__=(), __new__=new))
    globals()[name] = Class


def create_piece(kind, color):
    color = "White" if color == WHITE else "Black"
    name = {DRAUGHT: "Draught", PAWN: "ChessPawn", ROOK: "ChessRook",
            KNIGHT: "ChessKnight", BISHOP: "ChessBishop",
            KING: "ChessKing", QUEEN: "ChessQueen"}[kind]
    return globals()[color + name]()


class AbstractBoard:

    __classForPiece = {(DRAUGHT, BLACK): BlackDraught,
            (PAWN, BLACK): BlackChessPawn,
            (ROOK, BLACK): BlackChessRook,
            (KNIGHT, BLACK): BlackChessKnight,
            (BISHOP, BLACK): BlackChessBishop,
            (KING, BLACK): BlackChessKing,
            (QUEEN, BLACK): BlackChessQueen,
            (DRAUGHT, WHITE): WhiteDraught,
            (PAWN, WHITE): WhiteChessPawn,
            (ROOK, WHITE): WhiteChessRook,
            (KNIGHT, WHITE): WhiteChessKnight,
            (BISHOP, WHITE): WhiteChessBishop,
            (KING, WHITE): WhiteChessKing,
            (QUEEN, WHITE): WhiteChessQueen}

    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()

    def populate_board(self):
        raise NotImplementedError()

    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y+x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)


class CheckersBoard(AbstractBoard):

    def __init__(self):
        super().__init__(10, 10)

    def populate_board(self): # Thanks to Doug Hellmann for the idea!
        def black():
            return create_piece(DRAUGHT, BLACK)
        def white():
            return create_piece(DRAUGHT, WHITE)
        rows = ((None, black()), (black(), None), (None, black()),
                (black(), None),            # 4 black rows
                (None, None), (None, None), # 2 blank rows
                (None, white()), (white(), None), (None, white()),
                (white(), None))            # 4 white rows
        self.board = [list(itertools.islice(
            itertools.cycle(squares), 0, len(rows))) for squares in rows]


class ChessBoard(AbstractBoard):

    def __init__(self):
        super().__init__(8, 8)

    def populate_board(self):
        for row, color in ((0, BLACK), (7, WHITE)):
            for columns, kind in (((0, 7), ROOK), ((1, 6), KNIGHT),
                    ((2, 5), BISHOP), ((3,), QUEEN), ((4,), KING)):
                for column in columns:
                    self.board[row][column] = create_piece(kind, color)
        for column in range(8):
            for row, color in ((1, BLACK), (6, WHITE)):
                self.board[row][column] = create_piece(PAWN, color)


if __name__ == "__main__":
    main()
