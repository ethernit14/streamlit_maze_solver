# 🧩 Maze Solver - Streamlit Version

A visual comparison of three pathfinding algorithms: **DFS**, **BFS**, and **A*** with interactive maze generation and beautiful visualizations.

## Features

- 🎲 **Dynamic maze generation** with customizable size
- 🔍 **Three algorithms**: DFS, BFS, and A*
- 📊 **Side-by-side comparison** with timing and statistics
- 🎨 **Color-coded visualization** showing paths and explored cells
- ⚙️ **Customizable settings** (size, seed, multiple solutions)
- 📈 **Performance metrics** (steps, explored cells, execution time)

## How to Run

### Prerequisites
```bash
pip install streamlit numpy matplotlib
```

### Run the App
```bash
streamlit run streamlit_maze_solver.py
```

## Algorithms Explained

### Depth-First Search (DFS) 🔍
- Uses a **stack** (LIFO)
- Explores deep before backtracking
- Not guaranteed to find shortest path
- Memory efficient

### Breadth-First Search (BFS) 📊
- Uses a **queue** (FIFO)
- Explores all neighbors at current depth first
- **Guaranteed shortest path** in unweighted graphs
- Uses more memory

### A* (A-Star) ⭐
- Uses **priority queue** with heuristic
- Combines actual cost + estimated distance to goal
- **Most efficient** with good heuristic
- Guaranteed optimal path

## Features Explained

### Maze Settings
- **Width/Height**: Control maze dimensions (10-50)
- **Random Seed**: Reproducible mazes
- **Multiple Solutions**: Create alternative paths
- **Extra Paths Ratio**: How many alternate routes to add
- **Show Explored Cells**: Visualize algorithm efficiency

### Color Legend
- 🟢 **Green (Lime)**: Start position
- 🔴 **Red**: End position
- 🔵 **Cyan**: Solution path
- 🟡 **Yellow**: Explored cells (when enabled)
- ⚫ **Black**: Walls
- ⚪ **White**: Unvisited cells

## Files Included

- `streamlit_maze_solver.py` - Main Streamlit application
- `maze_generator.py` - Original maze generation logic
- `maze_solverdfs.py` - DFS solver
- `maze_solverbfs.py` - BFS solver
- `maze_solverastar.py` - A* solver
- `maze_comparison.py` - Original comparison script
- `README_STREAMLIT.md` - This file

## Original Version

Run the original comparison with:
```bash
python maze_comparison.py
```

This will generate matplotlib plots showing the algorithms.

## Tips

💡 Enable "Show Explored Cells" to see which cells each algorithm visited - A* typically explores fewer cells!

💡 Use a random seed for reproducible results and fair comparisons.

💡 Increase maze size for more interesting comparisons!

Enjoy solving mazes! 🧩
