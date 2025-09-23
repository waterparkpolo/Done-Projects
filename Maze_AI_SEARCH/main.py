import pygame
import sys
from maze import Maze
import algorithms

# --- Settings ---
ROWS, COLS = 21, 21
CELL_SIZE = 20
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + 80  # extra space for controls
BG_COLOR = (30, 30, 30)
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 215, 0)
VISITED_COLOR = (100, 200, 250)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
TEXT_COLOR = (240, 240, 240)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver AI (Animated)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

# Generate Maze
maze = Maze(ROWS, COLS)
grid = maze.get_grid()
start, end = maze.start, maze.end
path = []
visited_nodes = set()
solver = None  # generator

def draw_maze():
    for r in range(ROWS):
        for c in range(COLS):
            color = BG_COLOR if grid[r][c] == 0 else WALL_COLOR
            pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Visited cells
    for (r, c) in visited_nodes:
        pygame.draw.rect(screen, VISITED_COLOR, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Path
    for (r, c) in path:
        pygame.draw.rect(screen, PATH_COLOR, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Start & End
    pygame.draw.rect(screen, START_COLOR, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, END_COLOR, (end[1]*CELL_SIZE, end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_controls():
    instructions = [
        "Controls:",
        "1 = BFS   |   2 = DFS   |   3 = Dijkstra   |   4 = A*",
        "R = New Maze   |   ESC = Quit"
    ]
    y_offset = ROWS * CELL_SIZE + 10
    for i, text in enumerate(instructions):
        label = font.render(text, True, TEXT_COLOR)
        screen.blit(label, (10, y_offset + i*22))

def set_solver(algo_name):
    global solver, path, visited_nodes
    path = []
    visited_nodes = set()
    if algo_name == "BFS":
        solver = algorithms.bfs(grid, start, end)
    elif algo_name == "DFS":
        solver = algorithms.dfs(grid, start, end)
    elif algo_name == "Dijkstra":
        solver = algorithms.dijkstra(grid, start, end)
    elif algo_name == "A*":
        solver = algorithms.astar(grid, start, end)

def main():
    global solver, path, visited_nodes, maze, grid, start, end
    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_maze()
        draw_controls()
        pygame.display.flip()
        clock.tick(60)  # adjust speed here

        if solver is not None:
            try:
                node, visited = next(solver)
                visited_nodes = set(visited.keys())
                path = algorithms.reconstruct_path(visited, start, node)
            except StopIteration:
                solver = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    set_solver("BFS")
                elif event.key == pygame.K_2:
                    set_solver("DFS")
                elif event.key == pygame.K_3:
                    set_solver("Dijkstra")
                elif event.key == pygame.K_4:
                    set_solver("A*")
                elif event.key == pygame.K_r:
                    maze = Maze(ROWS, COLS)
                    grid = maze.get_grid()
                    start, end = maze.start, maze.end
                    path = []
                    visited_nodes = set()
                    solver = None

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()