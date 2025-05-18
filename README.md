# Maze Solver

This is a Python program that implements a maze solver using depth-first search (DFS) and breadth-first search (BFS). The solver reads a maze from a text file and finds a path from the start ('A') to the goal ('B').

## Features
- Reads a maze from a text file
- Supports DFS (stack-based) and BFS (queue-based) search strategies
- Prints the maze before and after solving
- Marks the solution path with `*`

## Requirements
- Python 3.x

## Usage

### 1. Prepare a Maze File
Create a maze by runnig `create.py` OR

Create a text file (e.g., `maze1.txt`) with:

- `A` representing the starting position.
- `B` representing the goal.
- `#` representing walls.
- Spaces (` `) representing open paths.

### 2. Run the Maze Solver
To solve the maze place your file in `gui.py` for GUI based representation OR

Execute the script to solve the maze:
```sh
python solve.py
```

### 3. Expected Output
The script prints the initial maze, solves it, and prints the solved maze with the solution path marked by `*`.

## File Structure
```
maze-solver/
│── solver.py         # Maze solver implementation
│── create.py         # Create you own maze
│── gui.py            # GUI based representation
│── solve.py          # Script to test the maze solver
│── maze1.txt         # Sample maze file
```