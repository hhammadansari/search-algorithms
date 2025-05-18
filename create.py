import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Start
RED = (255, 0, 0)    # Goal
GRAY = (200, 200, 200)

# Grid setup
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start = None
goal = None

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Builder - Phase 1")

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if grid[y][x] == 1:
                pygame.draw.rect(win, BLACK, rect)
            elif (y, x) == start:
                pygame.draw.rect(win, GREEN, rect)
            elif (y, x) == goal:
                pygame.draw.rect(win, RED, rect)
            else:
                pygame.draw.rect(win, WHITE, rect)

            pygame.draw.rect(win, GRAY, rect, 1)

def get_clicked_pos(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

def save_maze(filename="maze.txt"):
    with open(filename, "w") as f:
        for y in range(ROWS):
            line = ""
            for x in range(COLS):
                if (y, x) == start:
                    line += "A"
                elif (y, x) == goal:
                    line += "B"
                elif grid[y][x] == 1:
                    line += "#"
                else:
                    line += " "
            f.write(line + "\n")
    print(f"Maze saved to {filename}")

def main():
    global start, goal
    mode = None  # 'start' or 'goal'

    while True:
        draw_grid()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detect mode switching keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    mode = 'start'
                elif event.key == pygame.K_g:
                    mode = 'goal'
                elif event.key == pygame.K_RETURN:
                    save_maze()

            if pygame.mouse.get_pressed()[0]:  # Left Click
                pos = pygame.mouse.get_pos()
                y, x = get_clicked_pos(pos)
                if mode == 'start':
                    start = (y, x)
                    mode = None
                elif mode == 'goal':
                    goal = (y, x)
                    mode = None
                elif (y, x) != start and (y, x) != goal:
                    grid[y][x] = 1

            elif pygame.mouse.get_pressed()[2]:  # Right Click to erase
                pos = pygame.mouse.get_pos()
                y, x = get_clicked_pos(pos)
                if (y, x) == start:
                    start = None
                elif (y, x) == goal:
                    goal = None
                else:
                    grid[y][x] = 0

if __name__ == "__main__":
    main()
