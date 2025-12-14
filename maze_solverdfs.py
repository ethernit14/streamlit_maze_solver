import time

def dfs_solve(maze, start, end, return_visited=False):
    """Solve maze using DFS algorithm
    
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
    
    # Stack - LIFO
    stack = [start]
    
    # Track visited cells
    visited = set([start])
    
    # Parent tracking (to reconstruct the path)
    parent = {start: None}
    
    # 4 directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # DFS
    while stack:
        current = stack.pop()  # Get last element
        
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
            
            # Add to stack
            stack.append(neighbor)
            visited.add(neighbor)
            parent[neighbor] = current
    
    # No path found
    elapsed_time = time.time() - start_time
    return (None, visited, elapsed_time) if return_visited else None

