import numpy as np
from search_problem import Problem
from search_algorithms import *
from utility_functions import getClosestGold

#AStar_problem class which extends the generic Problem class and defines methods for an informed search
class A_star_problem(Problem):
    def __init__(self,initial, goal, actions, list_of_blocks, heuristic_function, wumpus, size, includeCostAction):
        self.heuristic_function=heuristic_function
        self.wumpus = wumpus
        self.includeCostAction=includeCostAction
        super().__init__(initial,goal, actions, list_of_blocks, size)

    #Given a node calculate its expansion returning the available_neighbors 
    def actions(self, node):
        available_neighbors=[]
        if self.is_valid(moveForward(node)):   
            #If given this position is possible to move forward wrt to the current direction add the move action     
            available_neighbors.append({'neighbor':moveForward(node),
                                        'action':[self.available_actions[0]], 
                                        'direction':node.direction, 
                                        'killedWumpuses': node.killedWumpuses})
        #Add left rotation
        available_neighbors.append({'neighbor':node.state,
                                    'action':[self.available_actions[2]],
                                    'direction':rotateLeft(node), 
                                    'killedWumpuses': node.killedWumpuses})
        #Add right rotation
        available_neighbors.append({'neighbor':node.state,
                                    'action':[self.available_actions[1]], 
                                    'direction':rotateRight(node), 
                                    'killedWumpuses': node.killedWumpuses})
        #If there is a wumpus in the neighboring cells shoot it
        if node.killedWumpuses == []:
            available_neighbors.append({'neighbor':node.state,
                                        'action':[self.available_actions[3]], 
                                        'direction':node.direction, 
                                        'killedWumpuses': killWumpuses(node, self.wumpus, self.size[0], self.size[1])})
        return available_neighbors
        

    #Function that returns the cost of actions made so far 
    def getCostOfActionsFighter(self,actions): 
        actions_value=[action.value for action in actions]
        #If the current actions include killing of the wumpus then return the cost of killing it (which is 10)
        #Otherwise return the cost of actions including the move operation (we take len of actions array since the cost for each operation of the fighter is 1)
        if(self.includeCostAction): #For evaluation purpose, compare the cost of the optimized path by taking into consideration the cost of moving the agent or not 
            return (len(actions)-1)+10 if 3 in actions_value else len(actions)
        return 10 if 3 in actions_value else 0
    
    #Function that calculates the cost of a given path
    def path_cost(self, path_cost, state, actions)->int:
        # Adds the cost of the path so far with the cost of the heuristic_function which estimates the cost from that node to the goal
        return path_cost+self.getCostOfActionsFighter(actions)+self.heuristic_function(state, self.goal[0])
        
    def goal_test(self, node):
        return not (super().goal_test(node.state) == False or (node.state in self.wumpus and node.state not in node.killedWumpuses))
    
#Kill wumpuses taking into consideration the position and direction of the agent
def killWumpuses(node, allWumpuses, widthOfGrid, heightOfGrid):
    killedWumpuses = []
    shootableCells = []
    if node.direction == "N":
        shootableCells = [(node.state[0], y) for y in range(node.state[1], heightOfGrid)]
    elif node.direction == "S":
        shootableCells = [(node.state[0], y) for y in range(0, node.state[1]+1)]
    elif node.direction == "O":
        shootableCells = [(x, node.state[1]) for x in range(0, node.state[0]+1)]
    elif node.direction == "E":
        shootableCells = [(x, node.state[1]) for x in range(node.state[0], widthOfGrid)]
    for wumpus in allWumpuses:
        if wumpus in shootableCells:
            killedWumpuses.append(wumpus)
    return killedWumpuses

def moveForward(node):
    direction_map = {
        "N": (0, 1),
        "S": (0, -1),
        "E": (1, 0),
        "O": (-1, 0)
    }
    return tuple(map(np.add, node.state, direction_map[node.direction]))

def rotateLeft(node):
    directions = ["N", "E", "S", "O"]
    return directions[(directions.index(node.direction) - 1) % len(directions)]
    
def rotateRight(node):
    directions = ["N", "E", "S", "O"]
    return directions[(directions.index(node.direction) + 1) % len(directions)]


def take_gold(eater_locations,gold,actions,list_of_blocks,heuristic_function,currentDirection, wumpus, size, killedWumpuses, includeCostAction):
    firstNode=Node(eater_locations, killedWumpuses= killedWumpuses, direction=currentDirection,parent=None, action=None,path_cost=0) 
    problem=A_star_problem(firstNode,[gold],actions,list_of_blocks, heuristic_function, wumpus, size, includeCostAction)
    solution, counter = graph_search(problem,Priority_Queue([firstNode]))
    if solution == None: 
        return [None, counter, []]
    return [solution, counter, solution.killedWumpuses]

 
#Function that runs the search problem. It is designed to potentially collect more than one gold and to have more than one wumpus
def A_star_runner(eater_locations,gold_locations,actions,list_of_blocks,heuristic_function, wumpus, size,includeCostAction):
    performedActions = []
    totalCounter = 0

    #Set the initial position of the fighter to N
    currentDirection = "N"
    #Variable to keep track if the kill action is yet used
    globalKilledWumpuses = []

    #Instantiate problem until no gold are available
    while len(gold_locations) > 0:
        closestGoldPos=getClosestGold(eater_locations, gold_locations, heuristic_function)
        solution, counter, killedWumpuses = take_gold(eater_locations, closestGoldPos, actions, list_of_blocks, heuristic_function, currentDirection, wumpus, size, globalKilledWumpuses,includeCostAction)
        globalKilledWumpuses = killedWumpuses
        #If the current gold cannot be reached, try to reach the next one and do not consider the current gold
        if solution == None: 
            gold_locations.remove(closestGoldPos)
            continue

        #Otherwise update the counter of the node visited
        totalCounter += counter
        #Update the actions to reach that gold
        performedActions += solution.solution()
        #Add the grap operation
        performedActions += [actions[4]]  
        #Set the currentDirection and the fighter position for the new problem (eventually for reaching the next gold)
        currentDirection = solution.direction
        gold_locations.remove(solution.state)
        eater_locations = solution.state

    #Return to the base
    #Instantiate a new problem for returning to the base
    solution,counter,shotWumpus = take_gold(eater_locations, (0,0), actions, list_of_blocks, heuristic_function, currentDirection, wumpus, size, globalKilledWumpuses,includeCostAction) 
    totalCounter += counter
    if solution == None:
        return performedActions
    performedActions += solution.solution()
    performedActions += [actions[5]] #climb action
    print("Number of visited nodes: ",str(totalCounter))
    return performedActions

 