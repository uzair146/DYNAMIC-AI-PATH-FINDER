import pygame
import heapq
import time
import random
import math

winW = 900
winH = 800
topH = 60
botH = 60
offX = 50
offY = topH + 20
cellSz = 25

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (173,216,230)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walkable = True
        self.isStart = False
        self.isGoal = False
        self.isFrontier = False
        self.isVisited = False
        self.isPath = False
        self.g = float(0)
        self.h = 0
        self.f = float(0)
        self.parent = None

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(x, y) for y in range(cols)] for x in range(rows)]
        self.start = self.cells[0][0]
        self.start.isStart = True
        self.goal = self.cells[rows-1][cols-1]
        self.goal.isGoal = True

    def setStart(self, x, y):
        if self.start:
            self.start.isStart = False
        self.start = self.cells[x][y]
        self.start.isStart = True
        self.start.walkable = True

    def setGoal(self, x, y):
        if self.goal:
            self.goal.isGoal = False
        self.goal = self.cells[x][y]
        self.goal.isGoal = True
        self.goal.walkable = True

    def randomObstacles(self, density):
        for row in self.cells:
            for cell in row:
                if cell.isStart or cell.isGoal:
                    continue
                cell.walkable = random.random() >= density

    def clearVisuals(self):
        for row in self.cells:
            for cell in row:
                cell.isFrontier = False
                cell.isVisited = False
                cell.isPath = False

    def resetCosts(self):
        for row in self.cells:
            for cell in row:
                cell.g = float(0)
                cell.h = 0
                cell.f = float(0)
                cell.parent = None

    def getCellFromPixel(self, x, y):
        gx = (x - offX) // cellSz
        gy = (y - offY) // cellSz
        if 0 <= gx < self.rows and 0 <= gy < self.cols:
            return self.cells[gx][gy]
        return None

def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def euclidean(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def search(grid, algo, heur, screen, font):
    startTime = time.time()
    start = grid.start
    goal = grid.goal
    grid.resetCosts()
    grid.clearVisuals()

    start.g = 0
    start.h = heur(start, goal)
    start.f = start.g + start.h if algo == "A*" else start.h

    frontier = []
    counter = 0
    heapq.heappush(frontier, (start.f, counter, start))
    start.isFrontier = True

    visited = set()
    visitedCnt = 0
    clock = pygame.time.Clock()

    while frontier:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        cur = heapq.heappop(frontier)[2]
        cur.isFrontier = False
        if cur in visited:
            continue
        visited.add(cur)
        visitedCnt += 1
        cur.isVisited = True

        drawGrid(screen, grid, font)
        pygame.display.flip()
        clock.tick(60)

        if cur == goal:
            path = []
            cost = 0
            while cur:
                path.append(cur)
                cur.isPath = True
                cur = cur.parent
                cost += 1
            path.reverse()
            for row in grid.cells:
                for c in row:
                    c.isFrontier = False
                    c.isVisited = False
            for c in path:
                c.isPath = True
            execTime = (time.time() - startTime) * 1000
            return path, visitedCnt, execTime, cost

        for nb in getNeighbors(grid, cur):
            if not nb.walkable or nb in visited:
                continue
            tentative = cur.g + 1
            if tentative < nb.g:
                nb.g = tentative
                nb.h = heur(nb, goal)
                nb.f = nb.g + nb.h if algo == "A*" else nb.h
                nb.parent = cur
                if not nb.isFrontier:
                    nb.isFrontier = True
                    counter += 1
                    heapq.heappush(frontier, (nb.f, counter, nb))

    execTime = (time.time() - startTime) * 1000
    return None, visitedCnt, execTime, 0

def getNeighbors(grid, cell):
    nb = []
    x, y = cell.x, cell.y
    if x > 0: nb.append(grid.cells[x-1][y])
    if x < grid.rows-1: nb.append(grid.cells[x+1][y])
    if y > 0: nb.append(grid.cells[x][y-1])
    if y < grid.cols-1: nb.append(grid.cells[x][y+1])
    return nb

def isPathBlocked(path, grid):
    if not path:
        return False
    return any(not c.walkable for c in path)

def spawnObstacle(grid, agentPos):
    for _ in range(100):
        x = random.randint(0, grid.rows-1)
        y = random.randint(0, grid.cols-1)
        c = grid.cells[x][y]
        if not c.isStart and not c.isGoal and c != agentPos and c.walkable:
            c.walkable = False
            return True
    return False

def drawGrid(screen, grid, font):
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (0, 0, winW, topH))
    info = f"Algo: {algo} | Heur: {heurName} | Dynamic: {'ON' if dyn else 'OFF'} | Nodes: {metrics['Nodes']} | Cost: {metrics['Cost']} | Time: {metrics['Time']} ms"
    screen.blit(font.render(info, True, WHITE), (10, 20))

    pygame.draw.rect(screen, BLACK, (0, winH - botH, winW, botH))
    instr = "Click: toggle obstacle | S: set start | G: set goal | SPACE: search | M: move | R: reset | A: toggle algo | H: toggle heur | D: toggle dynamic"
    screen.blit(font.render(instr, True, WHITE), (10, winH - botH + 10))

    for row in grid.cells:
        for c in row:
            rect = pygame.Rect(offX + c.y * cellSz, offY + c.x * cellSz, cellSz, cellSz)
            if not c.walkable:
                col = BLACK
            elif c.isStart:
                col = GREEN
            elif c.isGoal:
                col = RED
            elif c.isPath:
                col = BLUE
            elif c.isVisited:
                col = LIGHTBLUE
            elif c.isFrontier:
                col = YELLOW
            else:
                col = WHITE
            pygame.draw.rect(screen, col, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    pygame.display.flip()

def main():
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    pygame.init()
    screen = pygame.display.set_mode((winW, winH))
    pygame.display.set_caption("Dynamic Pathfinding")
    font = pygame.font.Font(None, 20)
    clock = pygame.time.Clock()

    grid = Grid(rows, cols)

    global algo, heurName, heurFunc, dyn, metrics
    algo = "A*"
    heurName = "Manhattan"
    heurFunc = manhattan
    dyn = False
    metrics = {"Nodes": 0, "Cost": 0, "Time": 0}

    agentPos = grid.start
    path = None
    setMode = None

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_s:
                    setMode = "start"
                elif e.key == pygame.K_g:
                    setMode = "goal"
                elif e.key == pygame.K_SPACE:
                    if grid.start and grid.goal:
                        path, vis, t, cost = search(grid, algo, heurFunc, screen, font)
                        metrics = {"Nodes": vis, "Cost": cost if path else "No path", "Time": f"{t:.2f}"}
                        drawGrid(screen, grid, font)
                elif e.key == pygame.K_m and path:
                    try:
                        idx = path.index(agentPos)
                    except:
                        agentPos = grid.start
                        path = None
                        grid.clearVisuals()
                        drawGrid(screen, grid, font)
                        continue
                    if idx == len(path)-1:
                        print("Already at goal")
                    else:
                        nxt = path[idx+1]
                        if not nxt.walkable:
                            # re-plan
                            oldStart = grid.start
                            grid.start = agentPos
                            agentPos.isStart = True
                            oldStart.isStart = False
                            newPath, vis, t, cost = search(grid, algo, heurFunc, screen, font)
                            grid.start = oldStart
                            oldStart.isStart = True
                            agentPos.isStart = False
                            if newPath:
                                path = newPath
                                metrics = {"Nodes": vis, "Cost": cost, "Time": f"{t:.2f}"}
                        else:
                            agentPos = nxt
                            if dyn and random.random() < 0.3:
                                spawnObstacle(grid, agentPos)
                                if path and isPathBlocked(path[idx+2:], grid):
                                    oldStart = grid.start
                                    grid.start = agentPos
                                    agentPos.isStart = True
                                    oldStart.isStart = False
                                    newPath, vis, t, cost = search(grid, algo, heurFunc, screen, font)
                                    grid.start = oldStart
                                    oldStart.isStart = True
                                    agentPos.isStart = False
                                    if newPath:
                                        path = newPath
                                        metrics = {"Nodes": vis, "Cost": cost, "Time": f"{t:.2f}"}
                        drawGrid(screen, grid, font)
                elif e.key == pygame.K_r:
                    agentPos = grid.start
                    path = None
                    grid.resetCosts()
                    grid.clearVisuals()
                    metrics = {"Nodes": 0, "Cost": 0, "Time": 0}
                    drawGrid(screen, grid, font)
                elif e.key == pygame.K_a:
                    algo = "GBFS" if algo == "A*" else "A*"
                    drawGrid(screen, grid, font)
                elif e.key == pygame.K_h:
                    if heurName == "Manhattan":
                        heurName = "Euclidean"
                        heurFunc = euclidean
                    else:
                        heurName = "Manhattan"
                        heurFunc = manhattan
                    drawGrid(screen, grid, font)
                elif e.key == pygame.K_d:
                    dyn = not dyn
                    drawGrid(screen, grid, font)

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                cell = grid.getCellFromPixel(e.pos[0], e.pos[1])
                if cell:
                    if setMode == "start":
                        grid.setStart(cell.x, cell.y)
                        agentPos = grid.start
                        path = None
                        setMode = None
                        grid.resetCosts()
                        grid.clearVisuals()
                        drawGrid(screen, grid, font)
                    elif setMode == "goal":
                        grid.setGoal(cell.x, cell.y)
                        path = None
                        setMode = None
                        grid.resetCosts()
                        grid.clearVisuals()
                        drawGrid(screen, grid, font)
                    elif not cell.isStart and not cell.isGoal:
                        cell.walkable = not cell.walkable
                        grid.resetCosts()
                        grid.clearVisuals()
                        path = None
                        drawGrid(screen, grid, font)

        drawGrid(screen, grid, font)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
