# Maze Solver

This is a Python program that implements a maze solver using depth-first search (DFS) and breadth-first search (BFS). The solver reads a maze from a text file and finds a path from the start ('A') to the goal ('B').

## Features
- Interactive Maze Builder (`create.py`)
- Supports DFS (stack-based) and BFS (queue-based) search strategies
-  Real-time visualization of explored and solution paths
- Difficulty rating based on nodes explored
- Text-based and graphical interface options
## Requirements
- Python 3.x
- `pygame` library  

Install pygame if you haven't:
```bash
pip install pygame
```

## Usage

### 1. Prepare a Maze File
Create a maze by runnig `create.py` :  

- Click to place/remove walls.
- Press `S` then click to place start.
- Press `G` then click to place goal.
- Press `Enter` to save the maze.  

OR

Create a text file (e.g., `maze1.txt`) with:

- `A` representing the starting position.
- `B` representing the goal.
- `#` representing walls.
- Spaces (` `) representing open paths.

### 2. Run the Maze Solver
To solve the maze place your file in `gui.py` for GUI based representation.  

Edit the last line of `gui.py` to switch algorithms:
```py
visualize("maze.txt", use_bfs=True)   # True for BFS, False for DFS
```

OR

Execute the script to solve the maze:
```sh
python solve.py
```

## File Structure
```
maze-solver/
│── solver.py         # Maze solver implementation
│── create.py         # Create you own maze
│── gui.py            # GUI based representation
│── solve.py          # Script to test the maze solver
│── maze1.txt         # Sample maze file
```