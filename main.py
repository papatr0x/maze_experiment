import arcade as arc
from grid import Border, Square, SQUARE_SIDE
from maze import DFSGeneration

# Set constants for the screen size
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Arcade Grid Example"
SCREEN_BG_COLOR = arc.color.SKY_BLUE

# grid config
GRID_SIDE = 40
MARGIN = 50

UPDATE_RATE = 0.003

class MyGame(arc.Window):
    """
    Main application class.
    """
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # grid config
        self.algorithm = None
        self.all_squares = None

        # Set the background color
        self.background_color = SCREEN_BG_COLOR

        self.step_delay = UPDATE_RATE
        # this warrants first on_update is executed
        self.time_since_last_step = self.step_delay

        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create a grid of squares
        self.all_squares = []
        
        if Square.sprites:
            Square.sprites.clear()
        else:
            Square.sprites = arc.SpriteList()

        if Border.sprites:
            Border.sprites.clear()
        else:
            Border.sprites = arc.SpriteList()

        # Create horizontal borders
        # There are (GRID_SIDE + 1) rows of horizontal borders
        h_borders = []
        for r in range(GRID_SIDE + 1):
            row_borders = []
            for c in range(GRID_SIDE):
                start = (MARGIN + c * SQUARE_SIDE, MARGIN + r * SQUARE_SIDE)
                end = (MARGIN + (c + 1) * SQUARE_SIDE, MARGIN + r * SQUARE_SIDE)
                border = Border(start, end)
                row_borders.append(border)
            h_borders.append(row_borders)

        # Create vertical borders
        # There are (GRID_SIDE + 1) columns of vertical borders
        v_borders = []
        for r in range(GRID_SIDE):
            row_borders = []
            for c in range(GRID_SIDE + 1):
                start = (MARGIN + c * SQUARE_SIDE, MARGIN + r * SQUARE_SIDE)
                end = (MARGIN + c * SQUARE_SIDE, MARGIN + (r + 1) * SQUARE_SIDE)
                border = Border(start, end)
                row_borders.append(border)
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

        start_square = self.all_squares[0][0]
        end_square = self.all_squares[GRID_SIDE-1][GRID_SIDE-1]
        start_square.color = end_square.color = arc.color.BLUE

        # instantiate generation algorithm
        self.algorithm = DFSGeneration(self.all_squares, start_square, end_square)


    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()

        # Batch draw all squares and borders
        if Square.sprites:
            Square.sprites.draw()

        if self.algorithm:
            # Highlight current square
            current = self.algorithm.current_square
            if current:
                center_x = current.x + current.side_length / 2
                center_y = current.y + current.side_length / 2
                arc.draw_rect_filled(arc.XYWH(center_x, center_y, current.side_length * 0.8, current.side_length * 0.8), arc.color.GREEN)

        if Border.sprites:
            Border.sprites.draw()

    def on_update(self, delta_time: float):
        """
        Update traversal logic.
        """
        self.time_since_last_step += delta_time
        
        # Process steps based on elapsed time to ensure speed even if FPS drops
        while self.time_since_last_step >= self.step_delay:
            self.time_since_last_step -= self.step_delay

            if self.algorithm:
                if not self.algorithm.step():
                    self.algorithm = None

                if not self.algorithm:
                    break

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
