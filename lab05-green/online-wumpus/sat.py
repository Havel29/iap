from z3 import *

def getSafeAndUnsafeCells(currentPosition, currentDimension, breeze_in, stench_in, visitedCells): 
    solver=Solver()

    stench_cells = [[Bool(f's_{i}_{j}') for j in range(currentDimension[0])] for i in range(currentDimension[0])]
    breeze_cells = [[Bool(f'b_{i}_{j}') for j in range(currentDimension[0])] for i in range(currentDimension[0])]
    pits_cells = [[Bool(f'p_{i}_{j}') for j in range(currentDimension[0])] for i in range(currentDimension[0])]
    wumpus_cells = [[Bool(f'w_{i}_{j}') for j in range(currentDimension[0])] for i in range(currentDimension[0])]


    #Facts
    for x, y in breeze_in:
        solver.add(breeze_cells[x][y])

    for x in range(currentDimension[0]):
        for y in range(currentDimension[0]):
            if (x,y) not in breeze_in and (x,y) in visitedCells:
                solver.add(breeze_cells[x][y] == False)
    
    for x, y in stench_in:
        solver.add(stench_cells[x][y])
    for x in range(currentDimension[0]):
        for y in range(currentDimension[0]):
            if (x,y) not in stench_in and (x,y) in visitedCells:
                solver.add(stench_cells[x][y] == False)
    

    #Constraints
    
    for i in range(currentDimension[0]):
        for j in range(currentDimension[0]):            
            neighbors = [(x, y) for x, y in [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)] if 0 <= x < currentDimension[0] and 0 <= y < currentDimension[0]]
            solver.add(Implies(breeze_cells[i][j], Or([pits_cells[x][y] for x, y in neighbors])))
            solver.add(Implies(stench_cells[i][j], Or([wumpus_cells[x][y] for x, y in neighbors])))
            solver.add(Implies(breeze_cells[i][j]==False, And(list([(pits_cells[x][y]==False) for x, y in neighbors]))))
            solver.add(Implies(stench_cells[i][j]==False, And(list([(wumpus_cells[x][y]==False) for x, y in neighbors]))))
    
    possiblePits = []
    possibleWumpus = []


    #Restrict the checks on the cells we are interested in
    neighbors = [(x, y) for x, y in [(currentPosition[0] - 1, currentPosition[1]), (currentPosition[0], currentPosition[1] - 1), (currentPosition[0], currentPosition[1] + 1), (currentPosition[0] + 1, currentPosition[1])] if 0 <= x < currentDimension[0] and 0 <= y < currentDimension[0]]

    while solver.check() == sat:
        model = solver.model()
        possibleWumpus += ([(i, j) for i in range(currentDimension[0]) for j in range(currentDimension[0]) if is_true(model[wumpus_cells[i][j]]) and (i,j) not in possibleWumpus if (i != currentDimension[0]-1 or j != currentDimension[0]-1) and (i,j) not in visitedCells])
        possiblePits += ([(i, j) for i in range(currentDimension[0]) for j in range(currentDimension[0]) if is_true(model[pits_cells[i][j]]) and (i,j) not in possiblePits if (i != currentDimension[0]-1 or j != currentDimension[0]-1) and (i,j) not in visitedCells])
        
        comparisons = []
        for scope in [pits_cells, wumpus_cells]:
            for neighbor in neighbors:
                comparisons += [scope[neighbor[0]][neighbor[1]] != is_true(model[scope[neighbor[0]][neighbor[1]]]) ]
        if comparisons:
            solver.add(Or(comparisons))
        else:
            break
    #print("possiblePits: ",possiblePits)
    #print("possibleWumpus: ",possibleWumpus)

    safe_cells = set()
    unsafe_cells = set()

    for i in range(currentDimension[0]):
        for j in range(currentDimension[0]):
            if  (i,j) in visitedCells: 
                continue
            if (i,j) not in possiblePits and (i,j) not in possibleWumpus and (i,j) in neighbors:
                safe_cells.add((i,j))
            elif ((i,j) in neighbors):
                unsafe_cells.add((i,j))

    return list(safe_cells), list(unsafe_cells), list(possibleWumpus)
