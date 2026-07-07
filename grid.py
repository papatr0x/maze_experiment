import arcade
from typing import NamedTuple

BORDER_COLOR = arcade.color.BLACK
VISITED_COLOR = arcade.color.WHITE
UNVISITED_COLOR = arcade.color.BLACK

BORDER_WIDTH = 2
SQUARE_SIDE = 15


class Border:
    """
    A class representing a border in the game.
    """

    sprites: arcade.SpriteList = None

    def __init__(self, start: tuple[float, float],
                 end: tuple[float, float],
                 active: bool = True):
        self.start_position = start
        self.end_position = end
        self._active = active

        # Determine orientation and length based on start and end positions
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        if abs(dx) >= abs(dy):
            # horizontal
            length = abs(dx)
            center_x = (start[0] + end[0]) / 2
            center_y = start[1]
            self.sprite = arcade.SpriteSolidColor(int(length), BORDER_WIDTH, center_x, center_y, color = BORDER_COLOR)
        else: # vertical case
            length = abs(dy)
            center_x = start[0]
            center_y = (start[1] + end[1]) / 2
            self.sprite = arcade.SpriteSolidColor(BORDER_WIDTH, int(length), center_x, center_y, color = BORDER_COLOR)

        self.sprite.visible = active
        Border.sprites.append(self.sprite)

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value
        if self.sprite:
            self.sprite.visible = value


class SquareBorders(NamedTuple):
    bottom: Border
    top: Border
    left: Border
    right: Border


class Square:
    """
    A class representing a square cell in the grid, composed of four borders.
    """

    sprites: arcade.SpriteList = None

    def __init__(
        self,
        x: float,
        y: float,
        row: int,
        col: int,
        side_length: float,
        bottom: Border,
        top: Border,
        left: Border,
        right: Border,
    ):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.side_length = side_length
        self._visited = False
        self._color = None
        self.borders = SquareBorders(bottom, top, left, right)

        self.sprite = arcade.SpriteSolidColor(SQUARE_SIDE,
                                              SQUARE_SIDE,
                                              x + SQUARE_SIDE / 2,
                                              y + SQUARE_SIDE / 2,
                                              color = arcade.color.GRAY_BLUE)
        Square.sprites.append(self.sprite)

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value: bool):
        self._visited = value
        if self.sprite:
            self._update_sprite_color()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        if self.sprite:
            self._update_sprite_color()

    def _update_sprite_color(self):
        if self._color:
            self.sprite.color = self._color
        else:
            self.sprite.color = VISITED_COLOR if self._visited else UNVISITED_COLOR

    def draw(self):
        """
        Draw the filled square.
        """
        center_x = self.x + self.side_length / 2
        center_y = self.y + self.side_length / 2

        color = self.color
        if self.color is None:
            color = VISITED_COLOR if self.visited else UNVISITED_COLOR

        arcade.draw_rect_filled(
            arcade.XYWH(center_x, center_y, self.side_length, self.side_length), color
        )
