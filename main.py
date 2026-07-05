import random
import arcade
from typing import NamedTuple

# Set constants for the screen size
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Arcade Grid Example"

BORDER_COLOR = arcade.color.BLACK
VISITED_COLOR = arcade.color.WHITE
UNVISITED_COLOR = arcade.color.GRAY

GRID_SIDE = 20
SQUARE_SIDE = 30
BORDER_WIDTH = 5
MARGIN = 50

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
        self.stack = None
        self.current_square = None
        self.end_square = None
        self.start_square = None
        self.all_squares = None
        self.all_borders = None
        self.background_color = arcade.color.SKY_BLUE

        self.step_delay = 0.01
        # this warrants first on_update is executed
        self.time_since_last_step = self.step_delay

        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.stack = None

        # Create a grid of squares
        self.all_squares = []
        self.all_borders = []

        # Create horizontal borders
        # There are (GRID_SIDE + 1) rows of horizontal borders
        h_borders = []
        for r in range(GRID_SIDE + 1):
            row_borders = []
            for c in range(GRID_SIDE):
                start = (MARGIN + c * SQUARE_SIDE, MARGIN + r * SQUARE_SIDE)
                end = (MARGIN + (c + 1) * SQUARE_SIDE, MARGIN + r * SQUARE_SIDE)
                border = Border(start, end, BORDER_WIDTH)
                row_borders.append(border)
                self.all_borders.append(border)
            h_borders.append(row_borders)

        # Create vertical borders
        # There are (GRID_SIDE + 1) columns of vertical borders
        v_borders = []
        for r in range(GRID_SIDE):
            row_borders = []
            for c in range(GRID_SIDE + 1):
                start = (MARGIN + c * SQUARE_SIDE, MARGIN + r * SQUARE_SIDE)
                end = (MARGIN + c * SQUARE_SIDE, MARGIN + (r + 1) * SQUARE_SIDE)
                border = Border(start, end, BORDER_WIDTH)
                row_borders.append(border)
                self.all_borders.append(border)
            v_borders.append(row_borders)

        # Create squares and assign borders
        for row in range(GRID_SIDE):
            square_row = []
            for col in range(GRID_SIDE):
                x = MARGIN + col * SQUARE_SIDE
                y = MARGIN + row * SQUARE_SIDE
                # bottom, top, left, right
                square = Square(
                    x, y, row, col, SQUARE_SIDE,
                    h_borders[row][col],
                    h_borders[row + 1][col],
                    v_borders[row][col],
                    v_borders[row][col + 1]
                )
                square_row.append(square)
            self.all_squares.append(square_row)

        self.start_square = self.all_squares[0][0]
        self.end_square = self.all_squares[GRID_SIDE-1][GRID_SIDE-1]

        self.start_square.color = self.end_square.color = arcade.color.BLUE

        # Initialize traversal state
        self.current_square = self.start_square
        self.current_square.visited = True
        self.stack = [self.current_square]

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

        # Highlight current square
        if self.stack:
            current = self.stack[-1]
            center_x = current.x + current.size / 2
            center_y = current.y + current.size / 2
            arcade.draw_rect_filled(arcade.XYWH(center_x, center_y, current.size * 0.8, current.size * 0.8), arcade.color.GREEN)

        # Draw all unique borders on top
        for border in self.all_borders:
            border.draw()

    def on_update(self, delta_time: float):
        """
        Update traversal logic.
        """
        self.time_since_last_step += delta_time
        if self.time_since_last_step < self.step_delay:
            return
        self.time_since_last_step -= self.step_delay

        if not self.stack:
            return

        # Get current square from the top of the stack
        current = self.stack[-1]

        # Find unvisited neighbors
        neighbors = []
        row, col = current.row, current.col

        # Directions: (d_row, d_col, border_name)
        directions = [
            (1, 0, 'top'),
            (-1, 0, 'bottom'),
            (0, -1, 'left'),
            (0, 1, 'right')
        ]

        for dr, dc, border_name in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_SIDE and 0 <= nc < GRID_SIDE:
                neighbor = self.all_squares[nr][nc]
                if not neighbor.visited:
                    neighbors.append((neighbor, border_name))

        if neighbors:
            # Pick a random unvisited neighbor
            next_square, border_name = random.choice(neighbors)

            # Deactivate the border between current and next square
            getattr(current.borders, border_name).active = False

            # Mark next square as visited and push to stack
            next_square.visited = True

            # once end_square is reached, pop it from stack to avoid additional roads to end square
            if next_square == self.end_square:
                self.stack.pop()
            else:
                self.stack.append(next_square)
        else:
            # No unvisited neighbors, backtrack by popping from stack
            self.stack.pop()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed. """
        if symbol == arcade.key.ESCAPE:
            self.close()
        elif symbol == arcade.key.R:
            self.setup()

def main():
    """ Main function """
    MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
