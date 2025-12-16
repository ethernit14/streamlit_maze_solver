import heapq
import time

def astar_solve(maze, start, end, return_visited=False):
    """Solve maze using A* algorithm
    
    Args:
        maze: The maze array
        start: Starting position tuple
        end: End position tuple
        return_visited: If True, returns (path, visited_set, elapsed_time)
    
    Returns:
        path or (path, visited, elapsed_time) if return_visited=True
    """
    start_time = time.time()
    
    height, width = maze.shape
    
    # Heuristic function (Manhattan distance)
    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    # Priority queue: (f_score, counter, position)
    # counter ensures FIFO ordering for equal f_scores
    counter = 0
    heap = [(heuristic(start), counter, start)]
    
    # Track visited cells
    visited = set()
    
    # G-score: cost from start to current node
    g_score = {start: 0}
    
    # Parent tracking (to reconstruct the path)
    parent = {start: None}
    
    # 4 directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # A* algorithm
    while heap:
        _, _, current = heapq.heappop(heap)
        
        # Skip if already visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # Did we reach the goal?
        if current == end:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path = path[::-1]  # Reverse
            elapsed_time = time.time() - start_time
            return (path, visited, elapsed_time) if return_visited else path
        
        # Check neighbors
        y, x = current
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)
            
            # Boundary check
            if not (0 <= ny < height and 0 <= nx < width):
                continue
            
            # Is it a wall?
            if maze[ny, nx] == 1:
                continue
            
            # Already visited?
            if neighbor in visited:
                continue
            
            # Calculate tentative g_score
            tentative_g = g_score[current] + 1
            
            # If this path is better than any previous one
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                counter += 1
                heapq.heappush(heap, (f_score, counter, neighbor))
                parent[neighbor] = current
    
    # No path found
    elapsed_time = time.time() - start_time
    return (None, visited, elapsed_time) if return_visited else None