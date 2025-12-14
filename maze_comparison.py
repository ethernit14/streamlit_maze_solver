import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from maze_generator import generate_maze
from maze_solverdfs import dfs_solve
from maze_solverbfs import bfs_solve
from maze_solverastar import astar_solve

def visualize(maze, start, end, dfs_path, bfs_path, astar_path, dfs_visited=None, bfs_visited=None, astar_visited=None, dfs_time=None, bfs_time=None, astar_time=None):
    """Visualize DFS vs BFS vs A* - with optional visited cells and timing"""
    dfs_display = maze.copy().astype(float)
    bfs_display = maze.copy().astype(float)
    astar_display = maze.copy().astype(float)
    
    # Show explored cells if provided
    if dfs_visited:
        for y, x in dfs_visited:
            if (y, x) not in [start, end] and maze[y, x] == 0:
                dfs_display[y, x] = 5
    if bfs_visited:
        for y, x in bfs_visited:
            if (y, x) not in [start, end] and maze[y, x] == 0:
                bfs_display[y, x] = 5
    if astar_visited:
        for y, x in astar_visited:
            if (y, x) not in [start, end] and maze[y, x] == 0:
                astar_display[y, x] = 5
    
    # Mark solution paths
    for y, x in dfs_path:
        if (y, x) not in [start, end]:
            dfs_display[y, x] = 4
    for y, x in bfs_path:
        if (y, x) not in [start, end]:
            bfs_display[y, x] = 4
    for y, x in astar_path:
        if (y, x) not in [start, end]:
            astar_display[y, x] = 4
    
    # Mark start and end
    dfs_display[start], bfs_display[start], astar_display[start] = 2, 2, 2
    dfs_display[end], bfs_display[end], astar_display[end] = 3, 3, 3
    
    # Plot - use different color lists for with/without visited cells
    if dfs_visited or bfs_visited or astar_visited:
        # Second figure: swap cyan and yellow so path=cyan, visited=yellow
        colors = ['white', 'black', 'lime', 'red', 'cyan', 'yellow']
    else:
        # First figure: swap red and yellow positions
        colors = ['white', 'black', 'lime', 'yellow', 'red', 'cyan']
    
    cmap = ListedColormap(colors)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 8))
    
    ax1.imshow(dfs_display, cmap=cmap, interpolation='nearest')
    title1 = f'DFS\nPath: {len(dfs_path)} steps'
    if dfs_visited:
        title1 += f' | Explored: {len(dfs_visited)} cells'
    if dfs_time is not None:
        title1 += f' | Time: {dfs_time:.6f}s'
    ax1.set_title(title1, fontweight='bold')
    ax1.axis('off')
    
    ax2.imshow(bfs_display, cmap=cmap, interpolation='nearest')
    title2 = f'BFS\nPath: {len(bfs_path)} steps'
    if bfs_visited:
        title2 += f' | Explored: {len(bfs_visited)} cells'
    if bfs_time is not None:
        title2 += f' | Time: {bfs_time:.6f}s'
    ax2.set_title(title2, fontweight='bold')
    ax2.axis('off')
    
    ax3.imshow(astar_display, cmap=cmap, interpolation='nearest')
    title3 = f'A*\nPath: {len(astar_path)} steps'
    if astar_visited:
        title3 += f' | Explored: {len(astar_visited)} cells'
    if astar_time is not None:
        title3 += f' | Time: {astar_time:.6f}s'
    ax3.set_title(title3, fontweight='bold')
    ax3.axis('off')
    
    legend_items = [('lime', 'Start'), ('red', 'End'), ('cyan', 'Path')]
    if dfs_visited or bfs_visited or astar_visited:
        legend_items.append(('yellow', 'Explored'))
    legend_items.extend([('black', 'Wall'), ('white', 'Unvisited')])
    
    fig.legend(handles=[Patch(facecolor=c, label=l) for c, l in legend_items],
               loc='lower center', ncol=6, fontsize=10)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.08)
    plt.show()

if __name__ == "__main__":
    # Generate and solve
    maze, start, end = generate_maze(width=20, height=20)
    dfs_path, dfs_visited, dfs_time = dfs_solve(maze, start, end, return_visited=True)
    bfs_path, bfs_visited, bfs_time = bfs_solve(maze, start, end, return_visited=True)
    astar_path, astar_visited, astar_time = astar_solve(maze, start, end, return_visited=True)
    
    # Check if paths were found
    if dfs_path is None or bfs_path is None or astar_path is None:
        print("No solution found! The maze might be unsolvable.")
        if dfs_path is None:
            print(f"DFS: No path found | Time: {dfs_time:.6f}s")
        if bfs_path is None:
            print(f"BFS: No path found | Time: {bfs_time:.6f}s")
        if astar_path is None:
            print(f"A*: No path found | Time: {astar_time:.6f}s")
    else:
        print(f"DFS: {len(dfs_path)} steps | Time: {dfs_time:.6f}s")
        print(f"BFS: {len(bfs_path)} steps | Time: {bfs_time:.6f}s")
        print(f"A*: {len(astar_path)} steps | Time: {astar_time:.6f}s")
        
        # First: show just paths
        visualize(maze, start, end, dfs_path, bfs_path, astar_path, dfs_time=dfs_time, bfs_time=bfs_time, astar_time=astar_time)
        
        # Second: show paths + exploration
        visualize(maze, start, end, dfs_path, bfs_path, astar_path, dfs_visited, bfs_visited, astar_visited, dfs_time, bfs_time, astar_time)
