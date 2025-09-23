from collections import deque
import heapq

# --- Pathfinding Algorithms as Generators ---
def bfs(grid, start, end):
    queue = deque([start])
    visited = {start: None}
    while queue:
        node = queue.popleft()
        yield node, visited
        if node == end:
            break
        for neighbor in neighbors(grid, node):
            if neighbor not in visited:
                visited[neighbor] = node
                queue.append(neighbor)
    yield from finish_path(visited, start, end)

def dfs(grid, start, end):
    stack = [start]
    visited = {start: None}
    while stack:
        node = stack.pop()
        yield node, visited
        if node == end:
            break
        for neighbor in neighbors(grid, node):
            if neighbor not in visited:
                visited[neighbor] = node
                stack.append(neighbor)
    yield from finish_path(visited, start, end)

def dijkstra(grid, start, end):
    pq = [(0, start)]
    visited = {start: None}
    dist = {start: 0}
    while pq:
        d, node = heapq.heappop(pq)
        yield node, visited
        if node == end:
            break
        for neighbor in neighbors(grid, node):
            new_dist = d + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                visited[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))
    yield from finish_path(visited, start, end)

def astar(grid, start, end):
    pq = [(0, start)]
    visited = {start: None}
    g = {start: 0}
    while pq:
        _, node = heapq.heappop(pq)
        yield node, visited
        if node == end:
            break
        for neighbor in neighbors(grid, node):
            tentative_g = g[node] + 1
            if neighbor not in g or tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, end)
                visited[neighbor] = node
                heapq.heappush(pq, (f, neighbor))
    yield from finish_path(visited, start, end)

# --- Helpers ---
def neighbors(grid, node):
    r, c = node
    moves = [(0,1),(0,-1),(1,0),(-1,0)]
    result = []
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0:
            result.append((nr,nc))
    return result

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(visited, start, end):
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = visited.get(node)
    path.reverse()
    return path if path and path[0] == start else []

def finish_path(visited, start, end):
    """Yield final reconstructed path so it can be drawn in yellow."""
    path = reconstruct_path(visited, start, end)
    for node in path:
        yield node, visited