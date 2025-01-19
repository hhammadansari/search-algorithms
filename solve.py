from maze import Maze

maze = Maze("maze1.txt")

print("Initial state:")
maze.print()

maze.solve()

print("Solved state:")
maze.print()