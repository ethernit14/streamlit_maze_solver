import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from collections import deque
from maze_generator import generate_maze

def bfs_solve(maze, start, end):
    """Solve maze using BFS algorithm"""
    height, width = maze.shape
    
    # Queue - FIFO
    queue = deque([start])
    
    # Track visited cells
    visited = set([start])
    
    # Parent tracking (to reconstruct the path)
    parent = {start: None}
    
    # 4 directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # BFS
    while queue:
        current = queue.popleft()  # Get first element
        
        # Did we reach the goal?
        if current == end:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse
        
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
            
            # Add to queue
            queue.append(neighbor)
            visited.add(neighbor)
            parent[neighbor] = current
    
    # No path found
    return None


def visualize_solution(maze, start, end, path=None):
    """Visualize the solution"""
    display = maze.copy().astype(float)
    
    # Draw the path
    if path:
        for (y, x) in path:
            if (y, x) != start and (y, x) != end:
                display[y, x] = 4  # Blue
    
    # Start and End
    display[start] = 2  # Green
    display[end] = 3    # Red
    
    # Colors
    colors = ['white', 'black', 'lime', 'red', 'cyan']
    cmap = ListedColormap(colors)
    
    # Plot
    plt.figure(figsize=(10, 10))
    plt.imshow(display, cmap=cmap, interpolation='nearest')
    plt.grid(True, which='both', color='gray', linewidth=0.5, alpha=0.3)
    
    if path:
        plt.title(f'BFS Solution - {len(path)} steps', fontsize=16)
    else:
        plt.title('No solution found!', fontsize=16)
    
    plt.tight_layout()
    plt.show()


# TEST
if __name__ == "__main__":
    print("🎮 Generating maze...")
    maze, start, end = generate_maze(width=20, height=20)
    
    print(f"Start: {start}, End: {end}")
    print(maze)
    
    print("\n🤖 Solving with BFS...")
    path = bfs_solve(maze, start, end)
    
    if path:
        print(f"✅ Solution found! {len(path)} steps")
    else:
        print("❌ No solution found!")
    
    # Visualize
    visualize_solution(maze, start, end, path)
