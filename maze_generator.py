import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
from collections import deque

def generate_maze(width=20, height=20, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    maze = np.ones((height, width), dtype=int)
    
    start = (0, 0)
    end = (height - 1, width - 1)
    
    # Use recursive backtracking to generate connected paths
    def carve_path(x, y):
        maze[y, x] = 0  # Mark as path
        
        # Define directions: right, down, left, up
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is valid and is a wall
            if 0 <= nx < width and 0 <= ny < height and maze[ny, nx] == 1:
                # Check if carving this path won't create a loop
                # Count neighboring paths (0s)
                neighbors = 0
                for ddx, ddy in directions:
                    nnx, nny = nx + ddx, ny + ddy
                    if 0 <= nnx < width and 0 <= nny < height and maze[nny, nnx] == 0:
                        neighbors += 1
                
                # Only carve if it won't create multiple connections
                if neighbors <= 1:
                    carve_path(nx, ny)
    
    # Start carving from the start position
    carve_path(start[0], start[1])
    
    # Ensure end position is also a path
    maze[end[1], end[0]] = 0
    
    # If end is isolated, carve a path to it
    if maze[end[1], end[0]] == 0:
        # Try to connect end to an existing path
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            nx, ny = end[0] + dx, end[1] + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny, nx] == 0:
                break
        else:
            # Force a connection if needed
            if end[1] > 0:
                maze[end[1] - 1, end[0]] = 0
    
    return maze, start, end

def display_maze(maze, path=None):
    cmap = ListedColormap(['white', 'black', 'red', 'blue'])
    display_maze = maze.copy()
    
    if path:
        for (y, x) in path:
            display_maze[y, x] = 2  # Mark path in red
        display_maze[path[0][0], path[0][1]] = 3  # Start in blue
        display_maze[path[-1][0], path[-1][1]] = 3  # End in blue
    
    plt.figure(figsize=(10, 10))
    plt.imshow(display_maze, cmap=cmap)
    plt.xticks([]), plt.yticks([])
    plt.show()
