from maze import Maze

maze = Maze("maze1.txt")

print("\nInitial state:")
maze.print()

maze.solve()

print("Solving...")

print("\nSolved state:")
maze.print()
print("States Explored:", maze.num_explored,"\n")