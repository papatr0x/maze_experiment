from random import choice
import arcade as arc
from grid import Border, Square

# Set constants for the screen size
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Arcade Grid Example"

# grid config
GRID_SIDE = 20
SQUARE_SIDE = 30
BORDER_WIDTH = 5
MARGIN = 50

class MyGame(arc.Window):
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
        self.background_color = arc.color.SKY_BLUE

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

        self.start_square.color = self.end_square.color = arc.color.BLUE

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
            arc.draw_rect_filled(arc.XYWH(center_x, center_y, current.size * 0.8, current.size * 0.8), arc.color.GREEN)

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
            next_square, border_name = choice(neighbors)

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
        if symbol == arc.key.ESCAPE:
            self.close()
        elif symbol == arc.key.R:
            self.setup()


def main():
    """ Main function """
    MyGame()
    arc.run()


if __name__ == "__main__":
    main()
