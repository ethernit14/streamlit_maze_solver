import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import random
from collections import deque
import heapq
import time

st.set_page_config(page_title="Maze Solver Comparison", page_icon="🧩", layout="wide")

# Maze Generator Functions
def generate_maze(width=20, height=20, seed=None, multiple_solutions=True, extra_paths_ratio=0.15):
    """Generate a maze with optional multiple solution paths."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    maze = np.ones((height, width), dtype=int)
    start = (0, 0)
    end = (height - 1, width - 1)
    
    def carve_path(x, y):
        maze[y, x] = 0
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny, nx] == 1:
                neighbors = 0
                for ddx, ddy in directions:
                    nnx, nny = nx + ddx, ny + ddy
                    if 0 <= nnx < width and 0 <= nny < height and maze[nny, nnx] == 0:
                        neighbors += 1
                if neighbors <= 1:
                    carve_path(nx, ny)
    
    carve_path(start[0], start[1])
    maze[end[1], end[0]] = 0
    
    if maze[end[1], end[0]] == 0:
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            nx, ny = end[0] + dx, end[1] + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny, nx] == 0:
                break
        else:
            if end[1] > 0:
                maze[end[1] - 1, end[0]] = 0
    
    if multiple_solutions:
        removable_walls = []
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if maze[y, x] == 1:
                    path_neighbors = 0
                    for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width and maze[ny, nx] == 0:
                            path_neighbors += 1
                    if path_neighbors >= 2:
                        removable_walls.append((y, x))
        
        num_to_remove = int(len(removable_walls) * extra_paths_ratio)
        walls_to_remove = random.sample(removable_walls, min(num_to_remove, len(removable_walls)))
        for y, x in walls_to_remove:
            maze[y, x] = 0
    
    return maze, start, end

# DFS Solver
def dfs_solve(maze, start, end):
    """Solve maze using DFS algorithm"""
    start_time = time.time()
    height, width = maze.shape
    stack = [start]
    visited = set([start])
    parent = {start: None}
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while stack:
        current = stack.pop()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            elapsed_time = time.time() - start_time
            return path[::-1], visited, elapsed_time
        
        y, x = current
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)
            if (0 <= ny < height and 0 <= nx < width and 
                maze[ny, nx] == 0 and neighbor not in visited):
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
    
    elapsed_time = time.time() - start_time
    return None, visited, elapsed_time

# BFS Solver
def bfs_solve(maze, start, end):
    """Solve maze using BFS algorithm"""
    start_time = time.time()
    height, width = maze.shape
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            elapsed_time = time.time() - start_time
            return path[::-1], visited, elapsed_time
        
        y, x = current
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)
            if (0 <= ny < height and 0 <= nx < width and 
                maze[ny, nx] == 0 and neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
    
    elapsed_time = time.time() - start_time
    return None, visited, elapsed_time

# A* Solver
def astar_solve(maze, start, end):
    """Solve maze using A* algorithm"""
    start_time = time.time()
    height, width = maze.shape
    
    def heuristic(pos):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    counter = 0
    heap = [(heuristic(start), counter, start)]
    visited = set()
    g_score = {start: 0}
    parent = {start: None}
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while heap:
        _, _, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            elapsed_time = time.time() - start_time
            return path[::-1], visited, elapsed_time
        
        y, x = current
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)
            
            if (0 <= ny < height and 0 <= nx < width and 
                maze[ny, nx] == 0 and neighbor not in visited):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor)
                    counter += 1
                    heapq.heappush(heap, (f_score, counter, neighbor))
                    parent[neighbor] = current
    
    elapsed_time = time.time() - start_time
    return None, visited, elapsed_time

# Visualization Function
def create_visualization(maze, start, end, paths, visited_cells=None, times=None, show_explored=False):
    """Create visualization of maze solutions"""
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    
    algorithm_names = ['DFS', 'BFS', 'A*']
    
    if show_explored and visited_cells:
        colors = ['white', 'black', 'lime', 'red', 'cyan', 'yellow']
    else:
        colors = ['white', 'black', 'lime', 'yellow', 'red', 'cyan']
    
    cmap = ListedColormap(colors)
    
    for idx, (ax, algo_name, path) in enumerate(zip(axes, algorithm_names, paths)):
        maze_display = maze.copy().astype(float)
        
        # Show explored cells if enabled
        if show_explored and visited_cells and visited_cells[idx]:
            for y, x in visited_cells[idx]:
                if (y, x) not in [start, end] and maze[y, x] == 0:
                    maze_display[y, x] = 5
        
        # Mark solution path
        if path:
            for y, x in path:
                if (y, x) not in [start, end]:
                    maze_display[y, x] = 4
        
        # Mark start and end
        maze_display[start] = 2
        maze_display[end] = 3
        
        # Plot
        ax.imshow(maze_display, cmap=cmap, interpolation='nearest')
        
        # Title with stats
        title = f'{algo_name}'
        if path:
            title += f'\nPath: {len(path)} steps'
        else:
            title += f'\nNo path found'
        
        if show_explored and visited_cells and visited_cells[idx]:
            title += f' | Explored: {len(visited_cells[idx])} cells'
        
        if times and times[idx] is not None:
            title += f'\nTime: {times[idx]:.6f}s'
        
        ax.set_title(title, fontweight='bold', fontsize=12)
        ax.axis('off')
    
    # Legend
    legend_items = [('lime', 'Start'), ('red', 'End'), ('cyan', 'Path')]
    if show_explored:
        legend_items.append(('yellow', 'Explored'))
    legend_items.extend([('black', 'Wall'), ('white', 'Unvisited')])
    
    fig.legend(handles=[Patch(facecolor=c, label=l) for c, l in legend_items],
               loc='lower center', ncol=6, fontsize=11)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    
    return fig

# Streamlit App
st.title("🧩 Maze Solver: Algorithm Comparison")
st.markdown("Compare **DFS**, **BFS**, and **A*** pathfinding algorithms visually!")

st.sidebar.header("⚙️ Maze Settings")

# Settings
width = st.sidebar.slider("Maze Width", 10, 50, 20, 5)
height = st.sidebar.slider("Maze Height", 10, 50, 20, 5)
use_seed = st.sidebar.checkbox("Use Random Seed", value=False)
seed = None
if use_seed:
    seed = st.sidebar.number_input("Seed", value=42, step=1)

multiple_solutions = st.sidebar.checkbox("Multiple Solution Paths", value=True)
if multiple_solutions:
    extra_paths = st.sidebar.slider("Extra Paths Ratio", 0.0, 0.3, 0.15, 0.05)
else:
    extra_paths = 0.0

show_explored = st.sidebar.checkbox("Show Explored Cells", value=False)

st.sidebar.markdown("---")
generate_button = st.sidebar.button("🎲 Generate & Solve New Maze", type="primary", use_container_width=True)

# Initialize session state
if 'maze' not in st.session_state or generate_button:
    with st.spinner("Generating maze and solving..."):
        maze, start, end = generate_maze(width, height, seed, multiple_solutions, extra_paths)
        
        # Solve with all algorithms
        dfs_path, dfs_visited, dfs_time = dfs_solve(maze, start, end)
        bfs_path, bfs_visited, bfs_time = bfs_solve(maze, start, end)
        astar_path, astar_visited, astar_time = astar_solve(maze, start, end)
        
        st.session_state.maze = maze
        st.session_state.start = start
        st.session_state.end = end
        st.session_state.paths = [dfs_path, bfs_path, astar_path]
        st.session_state.visited = [dfs_visited, bfs_visited, astar_visited]
        st.session_state.times = [dfs_time, bfs_time, astar_time]

# Display results
if 'maze' in st.session_state:
    paths = st.session_state.paths
    times = st.session_state.times
    
    # Check if solutions exist
    if all(p is None for p in paths):
        st.error("❌ No solution found! The maze might be unsolvable. Try generating a new one.")
    else:
        # Display stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🔍 DFS",
                f"{len(paths[0])} steps" if paths[0] else "No path",
                f"{times[0]:.6f}s"
            )
        
        with col2:
            st.metric(
                "📊 BFS",
                f"{len(paths[1])} steps" if paths[1] else "No path",
                f"{times[1]:.6f}s"
            )
        
        with col3:
            st.metric(
                "⭐ A*",
                f"{len(paths[2])} steps" if paths[2] else "No path",
                f"{times[2]:.6f}s"
            )
        
        st.markdown("---")
        
        # Create and display visualization
        fig = create_visualization(
            st.session_state.maze,
            st.session_state.start,
            st.session_state.end,
            paths,
            st.session_state.visited if show_explored else None,
            times,
            show_explored
        )
        
        st.pyplot(fig)
        plt.close()
        
        # Algorithm explanations
        with st.expander("📖 Algorithm Explanations"):
            st.markdown("""
            ### Depth-First Search (DFS) 🔍
            - Uses a **stack** (LIFO - Last In First Out)
            - Explores as far as possible along each branch before backtracking
            - **Not guaranteed** to find the shortest path
            - Memory efficient for deep mazes
            
            ### Breadth-First Search (BFS) 📊
            - Uses a **queue** (FIFO - First In First Out)
            - Explores all neighbors at the current depth before moving deeper
            - **Guaranteed** to find the shortest path (for unweighted graphs)
            - Uses more memory than DFS
            
            ### A* (A-Star) ⭐
            - Uses a **priority queue** with heuristic function
            - Combines actual cost from start + estimated cost to goal
            - **Guaranteed** to find the shortest path with an admissible heuristic
            - Most efficient when heuristic is good (Manhattan distance in this case)
            - Often explores fewer cells than BFS
            """)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Enable 'Show Explored Cells' to see which cells each algorithm visited!")
