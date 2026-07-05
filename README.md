# Maze Experiment

A simple toy project visualizing maze generation using a randomized Depth-First Search (DFS) algorithm, built with the [Python Arcade library](https://api.arcade.academy/).

## Features

- **Randomized DFS**: Generates a unique maze every time using the recursive backtracker algorithm.
- **Visual Traversal**: Watch the algorithm step through the grid in real-time.
- **Restart Functionality**: Press **'R'** to reset and start a new maze generation.
- **Customizable Speed**: Adjustable step delay for faster or slower visualization.

## Requirements

- Python 3.10 or higher
- [Arcade 3.x](https://api.arcade.academy/en/latest/install/index.html)

## Installation

This project uses `uv` for dependency management. If you have `uv` installed, you can run:

```bash
uv sync
```

Alternatively, you can install the dependencies via `pip`:

```bash
pip install arcade>=3.3.3
```

## How to Run

Execute the main script:

```bash
python main.py
```

Or using `uv`:

```bash
uv run main.py
```

## Controls

- **R**: Restart the maze generation.
- **ESC**: Close the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
