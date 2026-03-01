# Dynamic Pathfinding Agent

A graphical pathfinding simulator that lets you watch **Greedy Best‑First Search** and **A* Search** in action on a grid. 
You can add obstacles, change the start and goal, and even turn on **dynamic mode** where new obstacles appear while the agent moves 
forcing it to re‑plan in real time.


## Features

- **Interactive grid** – click to toggle obstacles.
- **Two search algorithms** – Greedy Best‑First (GBFS) and A*.
- **Two heuristics** – Manhattan and Euclidean distance.
- **Real‑time visualization** – frontier (yellow), visited (light blue), final path (blue).
- **Dynamic mode** – obstacles spawn randomly while the agent moves; if the path is blocked, the agent re‑plans automatically.
- **Keyboard controls** – all actions are performed via keys (no buttons).
- **Live metrics** – nodes visited, path cost, execution time displayed in the top bar.
- **Adjustable grid size** – enter rows and columns when starting.

---

## Requirements

- Python 3.6 or higher
- Pygame library

Install Pygame with:
```bash
pip install pygame
```

---

## How to Run

1. Save the code as `pathfinder.py`.
2. Open a terminal in that folder.
3. Run:
   ```bash
   python pathfinder.py
   ```
4. Enter the number of rows and columns when prompted.

---

## How to Use (Controls)

| Key | Action |
|-----|--------|
| **Click** | Toggle obstacle on/off (cannot toggle start/goal) |
| **S** | Enter **set start** mode – then click on a cell to make it the new start |
| **G** | Enter **set goal** mode – then click on a cell to make it the new goal |
| **SPACE** | Run the search with the current algorithm and heuristic |
| **M** | Move the agent **one step** along the current path. In dynamic mode, obstacles may appear after each move |
| **R** | Reset agent to start and clear the current path |
| **A** | Switch between **A\*** and **Greedy Best‑First** |
| **H** | Switch between **Manhattan** and **Euclidean** heuristic |
| **D** | Toggle **dynamic mode** on/off |

---

## Algorithms & Heuristics

### Greedy Best‑First Search (GBFS)
- Uses only the heuristic: `f(n) = h(n)`.
- Very fast, but **not guaranteed** to find the shortest path.
- Can get trapped in dead ends.

### A* Search
- Combines cost so far with the heuristic: `f(n) = g(n) + h(n)`.
- Always finds the **optimal (shortest) path** if the heuristic is admissible.
- Slightly more computations per node, but usually explores fewer nodes than GBFS in complex mazes.

### Heuristics
- **Manhattan**: `|x1-x2| + |y1-y2|` – best for 4‑directional movement.
- **Euclidean**: straight‑line distance – also admissible, but may be less accurate on a grid.

---

## Dynamic Mode

When dynamic mode is **ON**:
- After each agent move (press `M`), there is a **30% chance** a random walkable cell (excluding start, goal, and the agent’s current position) becomes an obstacle.
- If a new obstacle blocks any part of the **remaining path**, the agent immediately re‑plans from its current position using the same algorithm and heuristic.
- The updated path is shown in blue, and metrics are refreshed.

This simulates a changing environment, like a robot discovering new obstacles while moving.

---

## Visualization Colors

- **Green** – Start node  
- **Red** – Goal node  
- **Yellow** – Frontier (nodes waiting to be expanded)  
- **Light blue** – Visited (already expanded) nodes  
- **Blue** – Final path  
- **Black** – Obstacle (wall)  
- **White** – Free, unvisited cell  

---

## Metrics

The top bar displays:
- **Algorithm** (A* or GBFS)
- **Heuristic** (Manhattan or Euclidean)
- **Dynamic** (ON/OFF)
- **Nodes** – number of nodes expanded during the last search
- **Cost** – length of the found path (in steps), or "No path" if unreachable
- **Time (ms)** – execution time of the last search in milliseconds

---

## Project Structure (Simplified)

```
pathfinder.py
├── Cell class        – represents one grid cell
├── Grid class        – manages the 2D grid and helper methods
├── Heuristic functions – manhattan, euclidean
├── search()          – core search routine (works for both GBFS and A*)
├── getNeighbors()    – returns walkable neighbours of a cell
├── isPathBlocked()   – checks if a path is still valid
├── spawnObstacle()   – creates a random obstacle (dynamic mode)
├── drawGrid()        – renders everything with Pygame
└── main()            – event loop and user interaction
```

---

## Example Test Cases

You can try these scenarios to see the difference between GBFS and A*:

1. **Open field** – no obstacles: both find the path quickly, but A* expands a slightly wider band.
2. **Dead‑end trap** – place a wall that looks like a shortcut but leads to a dead end: GBFS will go into it and waste time; A* will avoid it because it considers the cost.
3. **Maze** – a complex layout: A* finds the optimal path; GBFS might take a longer route.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- Inspired by classic AI pathfinding algorithms.
- Built with Python and Pygame.

---

*Enjoy exploring pathfinding!*
