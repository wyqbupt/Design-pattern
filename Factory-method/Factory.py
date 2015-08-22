#!/usr/bin/env python3

import sys
import io
BLACK, WHITE = ("BLACK", "WHITE")

if sys.platform.startswith("win"):
    def console(char, background):
        return char or " "
    sys.stdout = io.StringIO()
else:
    def console(char, background):
        return "\x1B[{}m{}\x1B[0m".format(43 if background == BLACK else 47, char or " ")


class AbstractBoard:
    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns) for _ in range(rows)]]
        self.populate_board()

    def populate_board(self):
        raise NotImplementedError()

    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                squares = console(piece, BLACK if (y+x) % 2 else WHITE)
                squares.append("\n")
        return "".join(squares)


