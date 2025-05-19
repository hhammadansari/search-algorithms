import pygame
import time
from solver import *

CELL_SIZE = 30
FPS = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

file = "maze0.txt" # Change this to your maze file
maze = Maze(file)

def draw_maze(screen, maze, solution=None, explored=set()):
    for i in range(maze.height):
        for j in range(maze.width):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze.walls[i][j]:
                pygame.draw.rect(screen, BLACK, rect)
            elif (i, j) == maze.start:
                pygame.draw.rect(screen, GREEN, rect)
            elif (i, j) == maze.goal:
                pygame.draw.rect(screen, RED, rect)
            elif solution and (i, j) in solution:
                pygame.draw.rect(screen, YELLOW, rect)
            elif (i, j) in explored:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)


def evaluate_difficulty(explored_count, total_cells):
    ratio = explored_count / total_cells
    if ratio < 0.1:
        return "Very Easy, Try Again"
    elif ratio < 0.25:
        return "Easy, But Not Too Easy"
    elif ratio < 0.5:
        return "Medium, Not Bad"
    elif ratio < 0.75:
        return "Hard, Nice Job"
    else:
        return "Very Hard, Excellent Work"



def visualize(file, use_bfs=True):
    maze = Maze(file)
    pygame.init()
    screen = pygame.display.set_mode((maze.width * CELL_SIZE, maze.height * CELL_SIZE))
    pygame.display.set_caption("Maze Solver Visualization")
    clock = pygame.time.Clock()

    frontier = QueueFrontier() if use_bfs else StackFrontier()
    start = Node(state=maze.start, parent=None, action=None)
    frontier.add(start)
    explored = set()
    explored_count = 0

    while True:
        clock.tick(FPS)
        pygame.event.pump()
        draw_maze(screen, maze, explored=explored)
        pygame.display.flip()

        if frontier.empty():
            print("No solution found")
            break

        node = frontier.remove()
        explored.add(node.state)
        explored_count += 1

        if node.state == maze.goal:
            actions = []
            cells = []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            cells.reverse()
            draw_maze(screen, maze, solution=set(cells), explored=explored)
            pygame.display.flip()
            time.sleep(2)
            break

        for action, state in maze.neighbors(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

    difficulty = evaluate_difficulty(explored_count, maze.height * maze.width)
    print(f"\nStates Explored: {explored_count}")
    print(f"Difficulty Rating: {difficulty}")


if __name__ == '__main__':
    visualize(file, use_bfs=False)  # Change to False for DFS
