import arcade
from typing import NamedTuple

BORDER_COLOR = arcade.color.BLACK
VISITED_COLOR = arcade.color.WHITE
UNVISITED_COLOR = arcade.color.BLACK


class Border:
    """
    A class representing a border in the game.
    """
    def __init__(self, start_position: tuple[float, float],
                 end_position: tuple[float, float],
                 width: float,
                 color: tuple[int,int,int,int] = BORDER_COLOR,
                 active: bool = True):
        self.start_position = start_position
        self.end_position = end_position
        self.width = width
        self.color = color
        self.active = active

        # Determine orientation and length based on start and end positions
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]

        if abs(dx) >= abs(dy):
            self.orientation = 'H'
            self.length = abs(dx)
        else:
            self.orientation = 'V'
            self.length = abs(dy)

    def draw(self):
        """
        Draw the border using arcade.
        """
        if not self.active:
            return

        if self.orientation == 'H':
            # For horizontal borders, length is along X, width is thickness along Y
            center_x = (self.start_position[0] + self.end_position[0]) / 2
            center_y = self.start_position[1]
            arcade.draw_rect_filled(arcade.XYWH(center_x, center_y, self.length, self.width), self.color)
        else:
            # For vertical borders, length is along Y, width is thickness along X
            center_x = self.start_position[0]
            center_y = (self.start_position[1] + self.end_position[1]) / 2
            arcade.draw_rect_filled(arcade.XYWH(center_x, center_y, self.width, self.length), self.color)


class SquareBorders(NamedTuple):
    bottom: Border
    top: Border
    left: Border
    right: Border


class Square:
    """
    A class representing a square cell in the grid, composed of four borders.
    """

    def __init__(
        self,
        x: float,
        y: float,
        row: int,
        col: int,
        size: float,
        bottom: Border,
        top: Border,
        left: Border,
        right: Border,
    ):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.size = size
        self.visited = False
        self.color = None
        self.borders = SquareBorders(bottom, top, left, right)

    def draw(self):
        """
        Draw the filled square.
        """
        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2

        color = self.color
        if self.color is None:
            color = VISITED_COLOR if self.visited else UNVISITED_COLOR

        arcade.draw_rect_filled(
            arcade.XYWH(center_x, center_y, self.size, self.size), color
        )
