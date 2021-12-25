from pyamaze import maze, agent, textLabel, COLOR
from collections import deque


# the input of DFS function be:
#   1. the object of pyamaze
#   2. the postion of the start point (x-axis,y-axis)
def BFS(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    # create a deque to store the unvisited child cells
    frontier = deque()
    frontier.append(start)
    bfsPath = {}
    # create a list to store the visited cells
    explored = [start]
    bSearch = []

    # search until there is no path to reach the goal or until we reach the goal
    while len(frontier) > 0:
        currCell = frontier.popleft()
        if currCell == m._goal:
            break

        # explore each available naigabour cell or child cells
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                elif d == 'S':
                    childCell = (currCell[0]+1, currCell[1])
                elif d == 'N':
                    childCell = (currCell[0]-1, currCell[1])
                # if the cell is already visited -> ignore
                if childCell in explored:
                    continue
                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currCell
                bSearch.append(childCell)
    # print(f'{bfsPath}')

    # convert the backward path to a forward path from start to goal
    fwdPath = {}
    cell = m._goal
    while cell != (m.rows, m.cols):
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    return bSearch, bfsPath, fwdPath


if __name__ == '__main__':
    # create a 5x5 maze
    m = maze(5, 5)
    # we chose a maze to test all search algorithms on
    m.CreateMaze(loadMaze="maze--2021-12-24--19-27-15.csv")
    bSearch, bfsPath, fwdPath = BFS(m)

    # create (a, b, c) as agents
    a = agent(m, footprints=True, color=COLOR.green, shape='square')
    b = agent(m, footprints=True, color=COLOR.yellow,
              shape='square', filled=False)
    c = agent(m, 1, 1, footprints=True, color=COLOR.cyan,
              shape='square', filled=True, goal=(m.rows, m.cols))

    # create agent (d) to indicate the starting point
    d = agent(m, 5, 5, shape="square", filled=True, color=COLOR.yellow)

    # make agent a follow bfs search path
    m.tracePath({a: bSearch}, delay=100)
    # make (c) follow the backward path
    m.tracePath({c: bfsPath})
    # make (b) follow the optimal path
    m.tracePath({b: fwdPath})

    print("The solution path is:", fwdPath)

    l = textLabel(m, 'BFS Path Length', len(fwdPath)+1)
    l = textLabel(m, 'BFS Search Length', len(bSearch)+1)

    m.run()
