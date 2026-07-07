from typing import Protocol

from grid import Square, GRID_SIDE
from random import choice


class MazeAlgorithm(Protocol):
    """
    Common interface for maze algorithms.
    """

    @property
    def current_square(self) -> Square | None:
        """ Return the current square. """
        ...

    def step(self) -> bool:
        """ Perform a single step of the algorithm. """
        ...

class DFSGeneration(MazeAlgorithm):
    """
    Randomized DFS / recursive backtracker maze generation.
    """

    def __init__(
        self,
        squares: list[list[Square]],
        start_square: Square,
        end_square: Square
    ):
        self.squares = squares
        self.start_square = start_square
        self.end_square = end_square
        self.stack = [start_square]

        self.start_square.visited = True

        self.directions = [
            (1, 0, "top"),
            (-1, 0, "bottom"),
            (0, -1, "left"),
            (0, 1, "right"),
        ]

    @property
    def current_square(self) -> Square | None:
        if not self.stack:
            return None
        return self.stack[-1]

    def step(self) -> bool:
        if not self.stack:
            return False

        current = self.stack[-1]
        neighbors = []
        row, col = current.row, current.col

        for dr, dc, border_name in self.directions:
            nr, nc = row + dr, col + dc

            if 0 <= nr < GRID_SIDE and 0 <= nc < GRID_SIDE:
                neighbor = self.squares[nr][nc]

                if not neighbor.visited:
                    neighbors.append((neighbor, border_name))

        if neighbors:
            next_square, border_name = choice(neighbors)

            # Deactivate border
            if border_name == "top":
                current.borders.top.active = False
            elif border_name == "bottom":
                current.borders.bottom.active = False
            elif border_name == "left":
                current.borders.left.active = False
            elif border_name == "right":
                current.borders.right.active = False

            next_square.visited = True

            if next_square == self.end_square:
                self.stack.pop()
            else:
                self.stack.append(next_square)
        else:
            self.stack.pop()

        return bool(self.stack)