# Python Chess AI

A chess AI implementation using the `python-chess` library, featuring human vs AI gameplay with minimax algorithm and opening book support.

## Features

- 🏁 Human vs AI gameplay interface
- ⚙️ Advanced game evaluation with:
  - Piece value assessment
  - Position-based scoring tables
  - Quiescence search for stability
- 📖 Opening book support (Book.txt)
- 🧠 AI features:
  - Minimax algorithm with alpha-beta pruning
  - Move ordering optimization
  - Depth-limited search
  - Static position evaluation

## Requirements

- Python 3.6+
- python-chess library

Install dependencies:  
`pip install python-chess`

## Usage

1. Ensure `Book.txt` is in the working directory
2. Run the script:  
`python chess_ai.py`

**Game Controls:**
- Human moves are entered in UCI format (e.g., "e2e4")
- AI moves automatically calculated at depth 4
- Game follows standard chess rules and endings
 
 