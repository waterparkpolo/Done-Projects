import random

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.end = (rows - 1, cols - 1)
        self.generate()

    def generate(self):
        stack = [self.start]
        self.grid[self.start[0]][self.start[1]] = 0

        while stack:
            r, c = stack[-1]
            neighbors = []
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 1:
                    neighbors.append((nr, nc))

            if neighbors:
                nr, nc = random.choice(neighbors)
                self.grid[(r + nr) // 2][(c + nc) // 2] = 0
                self.grid[nr][nc] = 0
                stack.append((nr, nc))
            else:
                stack.pop()

    def get_grid(self):
        return self.grid