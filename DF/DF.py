# from pyamaze import maze, agent, textLabel, COLOR
from pyMaze import maze, agent, COLOR, textLabel


# the input of DFS function be:
#   1. the object of pyMaze
#   2. the postion of the start point (x-axis,y-axis)
def DFS(m, start=None):

    # in case if the user didnot input a position the,
    # function will start from the most right bottom
    if start is None:
        start = (m.rows, m.cols)

    # we add the start step in the explored list and head list
    explored = [start]
    check = [start]

    # we define the dfsPath, where the right final path will be saved
    dfsPath = {}
    # we define the Search path, where the search path will be saved,
    # that what provied the first path that shows the behavior of the search
    dSeacrh = []
    while len(check) > 0:
        # gitting the cell that will be checked
        currCell = check.pop()
        # adding the cell to the search list
        # to allow the program to show the behavior of the search
        dSeacrh.append(currCell)

        # if the goal stop, it can be changed to any value (x-axis, y-axis)
        if currCell == m._goal:
            break

        # poss value to check if there were more than one direction available,
        # so a red dot will be add
        poss = 0

        # a loop over the four directions, the algorithm give the priority for W->N->S->E,
        # and we check them in oppsite order so the W , for example be at the head of the check list
        for d in 'ESNW':
            # maze_map is the maze dictionary its indexes are (x,y) and
            # their values are the possible moves for example, {'E':0,'W':0,'S':1,'N':0} this says that only S,South, is open.
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    child = (currCell[0], currCell[1]+1)
                if d == 'W':
                    child = (currCell[0], currCell[1]-1)
                if d == 'N':
                    child = (currCell[0]-1, currCell[1])
                if d == 'S':
                    child = (currCell[0]+1, currCell[1])

                # in case the child have been checked no need to check it again
                if child in explored:
                    continue
                poss += 1
                explored.append(child)
                check.append(child)
                # compine the next cell, as an index, and the current cell, as a value of this index
                dfsPath[child] = currCell
        # as mentioned earlier, a red dot will appear if more than one direction are available
        if poss > 1:
            m.markCells.append(currCell)

    # we was compine the next cell, as an index, and the current cell, as a value of this index,
    # to avoide the overwriting if we have more than one possible direction.
    # in this dictionary only the right path will be saved
    fwdPath = {}
    # we start backward, from the goal to start
    cell = m._goal
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return dSeacrh, dfsPath, fwdPath


if __name__ == '__main__':
    m = maze(5, 5)  # can be Changed to any size

    # we chose a maze to test all search algorithms on
    m.CreateMaze(loadMaze="maze--2021-12-24--19-27-15.csv")

    # dSeacrh, dfsPath, fwdPath = DFS(m, (5, 5))
    # assigning the returned values of "DFS" function to the variables below
    dSeacrh, dfsPath, fwdPath = DFS(m)

    # create (a, b, c) as agents
    a = agent(m, footprints=True, color=COLOR.green,
              shape='square')
    b = agent(m, footprints=True, color=COLOR.yellow,
              shape='square', filled=False)
    c = agent(m, 1, 1, footprints=True, color=COLOR.cyan,
              shape='square', filled=True, goal=(m.rows, m.cols))

    # create agent (d) to indicate the starting point
    d = agent(m, 5, 5, shape="square", filled=True, color=COLOR.yellow)

    # make agent (a) follow DFS search path
    m.tracePath({a: dSeacrh})

    # make agent (c) follow DFS backward path
    m.tracePath({c: dfsPath})

    # make (b) follow the forward path
    m.tracePath({b: fwdPath})

    print("The solution path is:", fwdPath)

    l = textLabel(m, 'DFS Path Length', len(fwdPath)+1)
    l = textLabel(m, 'DFS Search Length', len(dSeacrh)+1)

    m.run()
