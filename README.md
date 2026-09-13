# Chess Engine

A local two-player chess game built with Python and Pygame. Click a piece, then click a legal square. The board tracks turns, filters illegal moves that leave your king in check, and ends the game on checkmate or stalemate.

There is also a random self-play simulator that picks legal moves for both sides.

## Features

- Standard starting position and all six piece types
- Legal-move generation (pawns, knights, bishops, rooks, queens, kings)
- Moves that would leave your own king in check are blocked
- Check, checkmate, and stalemate detection with on-screen results
- Click-to-move local play (White vs Black on one computer)
- Optional random self-play (`rsim`)
- Debug helpers to print the current board or the last saved state

## Requirements

- Python 3.9+
- [pygame](https://www.pygame.org/)
- [pywinstyles](https://pypi.org/project/pywinstyles/) (used to style the window title bar on Windows)

```bash
pip install pygame pywinstyles
```

## Run

From the project root:

```bash
python run.py
```

That launches the two-player game (`src/main.py`).

To watch random self-play instead, open `run.py` and swap the calls:

```python
if __name__ == "__main__":
    # main()
    rsim()
```

Then run `python run.py` again.

## Controls

| Input | Action |
| --- | --- |
| Left click | Select a piece, then select a destination |
| `P` | Print the current board to the terminal |
| `H` | Print the last saved board state |

## Project layout

```
ChessEngine/
├── run.py              # Entry point
├── assets/             # Piece sprites
└── src/
    ├── main.py         # Two-player Pygame loop
    ├── rsim.py         # Random self-play loop
    ├── board.py        # Board state, turns, check / mate
    └── piece.py        # Piece movement
```

## Status

Human vs computer is not implemented yet (`run.py` has a TODO for it). Special moves such as castling, en passant, and pawn promotion are also still out of scope.

## License

No license is attached to this repository yet. Add one if you want others to reuse the code.
