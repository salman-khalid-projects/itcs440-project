from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue


# h() function to calculate the heuristic values for cells
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))


# The A* algorithm
def aStar(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    # create open as an obj of priorityQueue which will priorities based on 3 values
    open = PriorityQueue()
    # first: the heuristic function value of the cell / second: manhatin distance( from cell to goal) / third: the cell itself
    open.put((h(start, m._goal), h(start, m._goal), start))
    aPath = {}

    # set the g_score to infinity to all cells except the starting cell
    g_score = {row: float("inf") for row in m.grid}
    # the g_score of the starting cell = zero
    g_score[start] = 0

    # set the f_score to infinity to all cells except the starting cell
    f_score = {row: float("inf") for row in m.grid}
    # the f-score of the starting cell is the heuristic function of the starting cell
    f_score[start] = h(start, m._goal)

    searchPath = [start]
    # search if the open is not empty or until we reach the goal. *Note the open will be empty if there is no path to reach the goal.*
    while not open.empty():
        currCell = open.get()[2]
        searchPath.append(currCell)
        if currCell == m._goal:
            break

        # explore each available naigabour cell or child cells
        # a loop over the four directions, the algorithm give the priority for W->N->S->E,
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                elif d == 'N':
                    childCell = (currCell[0]-1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0]+1, currCell[1])

                # calculate the g_score and f_score for the child cell
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, m._goal)

                # if the new score is better -> update score
                if temp_f_score < f_score[childCell]:
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_g_score + h(childCell, m._goal)
                    # put the info as 3-value tuple inside the open priority queue
                    open.put((f_score[childCell], h(
                        childCell, m._goal), childCell))

    # convert the backward path to a forward path from start to goal
    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return searchPath, aPath, fwdPath


if __name__ == '__main__':
    m = maze(4, 4)
    m.CreateMaze(loadMaze="maze--2021-12-24--19-27-15.csv")

    # assigning the returned values of "aStar" function to the variables below
    searchPath, aPath, fwdPath = aStar(m)

    # create (a, b, c) as agents
    a = agent(m, footprints=True, color=COLOR.green,
              shape='square')
    b = agent(m, footprints=True, color=COLOR.yellow,
              shape='square', filled=False)
    c = agent(m, 1, 1, footprints=True, color=COLOR.cyan,
              shape='square', filled=True, goal=(m.rows, m.cols))
    # create agent (d) to indicate the starting point
    d = agent(m, 5, 5, shape="square", filled=True, color=COLOR.yellow)

    # tracePath function shows the content ,cells visited, of those lists in order causing this motion in the maze
    # make agent a follow A* search path
    m.tracePath({a: searchPath}, delay=300)
    # make (c) follow the backward path
    m.tracePath({c: aPath}, delay=300)
    # make (b) follow the forward path
    m.tracePath({b: fwdPath}, delay=300)

    print("The solution path is:", fwdPath)

    l = textLabel(m, 'A Star Path Length', len(fwdPath)+1)
    l = textLabel(m, 'A Star Search Length', len(searchPath))
    m.run()
