from typing import NamedTuple

import arcade

# Set constants for the screen size
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Arcade Grid Example"

BORDER_COLOR = arcade.color.BLACK
VISITED_COLOR = arcade.color.WHITE
UNVISITED_COLOR = arcade.color.GRAY

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
            self.orientation = "horizontal"
            self.length = abs(dx)
        else:
            self.orientation = "vertical"
            self.length = abs(dy)

    def draw(self):
        """
        Draw the border using arcade.
        """
        if not self.active:
            return

        if self.orientation == "horizontal":
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
    def __init__(self, x: float, y: float,
                 row: int, col: int,
                 size: float,
                 bottom: Border, top: Border, left: Border, right: Border):
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

        arcade.draw_rect_filled(arcade.XYWH(center_x, center_y, self.size, self.size), color)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background color
        self.background_color = arcade.color.SKY_BLUE

        # Create a grid of squares
        self.all_squares = []
        self.all_borders = []
        grid_size = 20
        square_side = 30
        border_width = 5
        margin = 50

        # Create horizontal borders
        # There are (grid_size + 1) rows of horizontal borders
        h_borders = []
        for r in range(grid_size + 1):
            row_borders = []
            for c in range(grid_size):
                start = (margin + c * square_side, margin + r * square_side)
                end = (margin + (c + 1) * square_side, margin + r * square_side)
                border = Border(start, end, border_width)
                row_borders.append(border)
                self.all_borders.append(border)
            h_borders.append(row_borders)

        # Create vertical borders
        # There are (grid_size + 1) columns of vertical borders
        v_borders = []
        for r in range(grid_size):
            row_borders = []
            for c in range(grid_size + 1):
                start = (margin + c * square_side, margin + r * square_side)
                end = (margin + c * square_side, margin + (r + 1) * square_side)
                border = Border(start, end, border_width)
                row_borders.append(border)
                self.all_borders.append(border)
            v_borders.append(row_borders)

        # Create squares and assign borders
        for row in range(grid_size):
            square_row = []
            for col in range(grid_size):
                x = margin + col * square_side
                y = margin + row * square_side
                # bottom, top, left, right
                square = Square(
                    x, y, row, col, square_side,
                    h_borders[row][col],
                    h_borders[row + 1][col],
                    v_borders[row][col],
                    v_borders[row][col + 1]
                )
                square_row.append(square)
            self.all_squares.append(square_row)

        start_square = self.all_squares[0][0]
        end_square = self.all_squares[grid_size-1][grid_size-1]

        start_square.color = end_square.color = arcade.color.RED

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color and erase what we drew last frame.
        self.clear()

        # Draw the square fills first
        for row in self.all_squares:
            for square in row:
                square.draw()

        # Draw all unique borders on top
        for border in self.all_borders:
            border.draw()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed. """
        if symbol == arcade.key.ESCAPE:
            self.close()

def main():
    """ Main function """
    MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
