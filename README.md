# Search Algorithms - Maze Solver (BFS vs DFS)

A Python maze solver that finds a path from a start cell to a goal cell using either Breadth-First Search (BFS) or Depth-First Search (DFS), with a Pygame visualization of which cells get explored and the final path found, plus a separate tool for building your own maze layouts by hand.

This is an educational project built to understand uninformed graph search.

## Table of contents
 
- [Overview](#overview)
- [Why BFS vs DFS?](#why-bfs-vs-dfs)
- [How the solver works](#how-the-solver-works)
- [Features](#features)
- [Switching between BFS and DFS](#switching-between-bfs-and-dfs)
- [Interactive Maze Builder (`create.py`)](#interactive-maze-builder-createpy)
- [Maze representation](#maze-representation)
- [Visualization (`gui.py`)](#visualization-guipy)
- [Difficulty rating](#difficulty-rating)
- [BFS vs. DFS — what you'll actually observe](#bfs-vs-dfs--what-youll-actually-observe)
- [Installation](#installation)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Complexity](#complexity)
- [What this project demonstrates](#what-this-project-demonstrates)

## Overview

A maze is represented as a grid of walls, open space, a start (`A`), and a goal (`B`). The solver treats each open cell as a graph node connected to its up/down/left/right open neighbors, and searches that graph for a path from `A` to `B` using one of two classic uninformed search strategies:

- **BFS**: explores the maze level-by-level, outward from the start.
- **DFS**: explores as far as possible down one path before backtracking.

The project exists to make the *difference* between these two visible and concrete: same maze, same neighbor logic, only the data structure holding the frontier changes (a queue vs. a stack) and that one change produces a visibly different exploration pattern and, usually, a different path.

## Why BFS vs DFS?

Both algorithms explore the same grid using the same `neighbors()` logic. The only difference in this implementation is which data structure holds the frontier of "cells to visit next":

### BFS (`QueueFrontier`)

- Removes the **oldest**-added node first (FIFO), so it visits all cells at distance 1 from the start, then all cells at distance 2, and so on.
- Because it expands outward one full "ring" at a time, the first time it reaches the goal, it has done so via the shortest possible route, this holds for this implementation because every move costs the same (one step in any of 4 directions), i.e. an unweighted grid.
- Time and space: **O(V + E)**, where `V` is the number of open (non-wall) cells and `E` is the number of open adjacent-cell pairs. In the worst case the frontier and explored set can hold close to every open cell.

### DFS (`StackFrontier`)

- Removes the **most recently**-added node first (LIFO), so it commits to one direction and keeps going until it hits a dead end, then backtracks.
- It is **not** guaranteed to find the shortest path, it finds *a* path, and which one depends entirely on the order neighbors are checked
  (`up, down, left, right` in this code).
- Time and space: **O(V + E)** as well, same asymptotic bound as BFS, but in practice DFS's frontier tends to stay smaller than BFS's mid-search, since it isn't holding an entire growing "ring" of cells at once.

| Property | BFS (`QueueFrontier`) | DFS (`StackFrontier`) |
|---|---|---|
| Data structure | Queue (FIFO) | Stack (LIFO) |
| Shortest path | Yes, on this unweighted grid | Not guaranteed |
| Exploration pattern | Outward, ring by ring | Deep along one branch, then backtrack |
| Time complexity | O(V + E) | O(V + E) |
| Space complexity | O(V) | O(V) |

## How the solver works

```text
Maze text file
      ↓
Parse into a wall/open grid, locate A (start) and B (goal)
      ↓
Initialize frontier with the start node
      ↓
Loop: remove one node from the frontier
      ↓
Is it the goal? - yes ──→ walk parent pointers back to start → reverse → done
      │ no
      ↓
Mark it explored, look up its open neighbors
      ↓
Add any neighbor not already explored/queued, back to "Loop"
```

Concretely, in `solver.py`:

- **`Maze.__init__`** reads the file, requires exactly one `A` and one `B` (raises an exception otherwise), and builds `self.walls`, a 2D list of booleans (`True` = wall).
- **`Node`** stores a `(row, col)` state, a reference to its parent node, and the action taken to reach it, this parent chain is what makes path reconstruction possible.
- **`StackFrontier`** / **`QueueFrontier`** hold the nodes waiting to be explored; they differ only in whether `remove()` pops from the end (stack) or the front (queue).
- **`Maze.neighbors(state)`** returns the valid up/down/left/right moves from a cell, skipping walls and out-of-bounds positions.
- **`Maze.solve()`** runs the loop above, tracking `self.explored` (a set, so already-visited cells are never re-queued) and `self.num_explored` (a running count of how many nodes were removed from the frontier).

## Features

- BFS and DFS maze solving, sharing the same `Maze`/`Node`/neighbor logic.
- Text-based maze format (see below), easy to write or generate mazes by hand.
- Terminal output: prints the maze before and after solving, with the path marked as `*` (`solve.py`).
- Pygame visualization: animates the search cell-by-cell and highlights the final path (`gui.py`).
- A separate interactive maze builder for drawing your own mazes with the mouse (`create.py`).
- Four sample mazes of increasing size (`maze0.txt`–`maze3.txt`).

## Switching between BFS and DFS

**`gui.py` (visualization):** open `gui.py` and find the last line of the
file:
 
```python
if __name__ == '__main__':
    visualize(file, use_bfs=False)  # Change to False for DFS
```
 
- `use_bfs=True` → BFS
- `use_bfs=False` → DFS (this is the current default)

Change the value, save, and re-run `python gui.py`.
 
**`solve.py` (terminal version):** this one doesn't take a `use_bfs`
argument at all, the algorithm is fixed inside `Maze.solve()` in
`solver.py`. Open `solver.py` and find this line inside `solve()`:
 
```python
frontier = QueueFrontier() # Change it to QueueFrontier() for BFS (Breadth-First Search)
```

- `QueueFrontier()` → BFS (this is the current default)
- `StackFrontier()` → DFS

Change the class name, save, and re-run `python solve.py`. Note that this
edit affects `solve.py` only. `gui.py` has its own independent `use_bfs`
switch and reading `solver.py`'s frontier line has no effect on it.

## Interactive Maze Builder (`create.py`)

Opens a 600×600 window with a fixed **20×20** grid. Controls:

| Input | Effect |
|---|---|
| `S` then left-click a cell | Set that cell as the **start** (green) |
| `G` then left-click a cell | Set that cell as the **goal** (red) |
| Left-click (no mode active) | Place a **wall** (black) |
| Right-click | Erase - clears a wall, or removes start/goal if you click on it |
| `Enter` | Save the current grid to `maze.txt` |

## Maze representation

Plain text, one line per row:

- `A` - start (must appear exactly once)
- `B` - goal (must appear exactly once)
- `#` - wall
- ` ` (space) - open, walkable cell

Example (`maze1.txt`, included in the repo):

```text
#####B#
##### #
####  #
#### ##
     ##
A######
```

Rows don't need to be the same length - `Maze.__init__` uses the longest line as the grid width and treats any missing characters on shorter rows as open space.

## Visualization (`gui.py`)

Each cell is drawn as a colored square, with the color depending on its current state during the search:

| Color | Meaning |
|---|---|
| Black | Wall |
| Green | Start |
| Red | Goal |
| Blue | Explored (has been removed from the frontier) |
| Yellow | Final solution path (drawn once the goal is found) |
| White | Unvisited open cell |

The window redraws at 15 FPS, so you see cells turn blue one at a time as the search progresses, this is what actually makes the BFS "ring by ring" vs. DFS "one long branch" difference visible rather than just theoretical. Once the goal is reached, the path is drawn in yellow and the window closes automatically after a 2-second pause.

Which maze file is loaded (`file = "maze0.txt"`) and which algorithm runs (`visualize(file, use_bfs=False)`, at the bottom of `gui.py`) are both set by editing those two lines directly.

## Difficulty rating

`gui.py` computes `explored_count / (maze.height * maze.width)` after solving and buckets the result into one of five labels (from "Very Easy" to "Very Hard, Excellent Work").

Worth being precise about what this actually measures: it is **not** an objective measure of how hard a maze is to navigate. It's the number of cells the *specific search run* ended up removing from the frontier, divided by the *total* grid area, walls included, not just walkable cells. Note that: (1) the same maze can score differently under BFS vs. DFS, since they explore different numbers of cells to reach the same goal, and (2) a maze that's mostly walls will structurally score "easier" than an equally-convoluted maze with fewer walls, purely because the denominator is larger. It's best understood as a rough, algorithm-dependent proxy for search effort on a given run, not a property of the maze itself.

## BFS vs. DFS - what you'll actually observe

Running the same maze through both algorithms (by editing the frontier type in `solver.py`, or `use_bfs` in `gui.py`) will typically show:

- BFS explores more cells overall (it fans out in every direction before committing), but the path it returns is the shortest one available.
- DFS often explores fewer cells to *reach* the goal, but the returned path can be noticeably longer or more winding, since it follows whichever direction it committed to first.

## Installation

```bash
git clone https://github.com/hhammadansari/search-algorithms.git
cd search-algorithms
pip install pygame
```

`solve.py` and `solver.py` use only the standard library; `pygame` is only
needed for `create.py` and `gui.py`. There's no `requirements.txt` in the
repo currently - `pygame` is the one external dependency.

## Usage

**Solve a maze in the terminal (BFS only, as currently written):**
```bash
python solve.py
```
This loads `maze3.txt` (hardcoded at the top of the file), prints the maze,
solves it, prints the solved maze with the path marked as `*`, and prints
the number of states explored.

**Solve a maze with the visualization:**
```bash
python gui.py
```
This loads whichever file and algorithm are set at the top/bottom of
`gui.py` (`maze0.txt` and DFS by default, currently).

**Build your own maze:**
```bash
python create.py
```
Draw a maze as described above, then press `Enter` to write it to
`maze.txt`.

## Project structure

| File | Responsibility |
|---|---|
| `solver.py` | Core logic: `Node`, `StackFrontier`/`QueueFrontier`, and the `Maze` class (parsing, neighbor lookup, and `solve()`). No dependency on Pygame. |
| `solve.py` | Minimal terminal entry point - loads one hardcoded maze, solves it with BFS, prints before/after. |
| `gui.py` | Pygame visualization - animates the search and draws the final path; supports switching to DFS via a variable. |
| `create.py` | Standalone Pygame tool for drawing a maze and saving it to a text file. Not connected to `solver.py`. |
| `maze0.txt`–`maze3.txt` | Sample mazes, increasing in size and complexity. |

## Complexity

For both BFS and DFS: **O(V + E)** time and **O(V)** space, where:
- `V` = number of open (non-wall) cells in the maze - each is a graph node.
- `E` = number of open adjacent-cell pairs - each cell has up to 4 edges
  (up/down/left/right), so `E` is at most `4V`, making `O(V + E)` equivalent
  to `O(V)` here.

In practice, the *constant* behind that bound differs a lot between BFS and
DFS depending on maze shape (see "BFS vs. DFS, what you'll actually
observe" above), the asymptotic complexity is the same, but the actual
number of cells explored on a given maze usually isn't.

## What this project demonstrates

- Graph traversal on an implicit grid graph (no explicit graph object; edges
  are computed on demand via `neighbors()`).
- The practical difference a frontier's data structure (stack vs. queue)
  makes to search behavior, using two algorithms that are otherwise
  identical.
- Path reconstruction via parent pointers, rather than storing full paths at
  every node.
- Visited-state tracking to avoid re-exploring or infinite-looping.
- Basic Pygame event handling and grid rendering (both `create.py` and
  `gui.py`).
