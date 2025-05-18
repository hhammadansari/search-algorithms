from solver import Maze

maze = Maze("maze3.txt")

print("\nInitial state:")
maze.print()

maze.solve()

print("Solving...")

print("\nSolved state:")
maze.print()
print("States Explored:", maze.num_explored,"\n")
