import numpy as np
from search_problem import Problem
from search_algorithms import *

class Dfs_problem(Problem):
    def __init__(self,initial, goal, actions, list_of_blocks, depth):
        self.depth = depth
        super().__init__(initial,goal, actions, list_of_blocks)

def dfs_runner(eater_locations,food_locations,actions,list_of_blocks):
    firstNode=Node(eater_locations, parent=None, action=None)
    problem=Dfs_problem(firstNode,food_locations,actions,list_of_blocks)
    solution=graph_search(problem,StackFrontier([firstNode]))
    return solution.solution()

def eat_banana(eater_locations,food_locations,actions,list_of_blocks):
    depth=0
    solution=None
    counter = 0
    while(depth!=100):        
        firstNode=Node(eater_locations, parent=None, action=None)
        problem=Dfs_problem(firstNode,food_locations,actions,list_of_blocks,depth)
        solution,counter=graph_search(problem,StackFrontier([firstNode]))
        if(solution==None or solution==[]):
            depth+=1
        else:
            return solution,counter
    return solution, counter

def iterative_deepening_runner(eater_locations,food_locations,actions,list_of_blocks):
    monkeyActions = []
    totalCounter = 0
    while len(food_locations) > 0:
        solution, counter = eat_banana(eater_locations, food_locations, actions, list_of_blocks)
        totalCounter += counter
        monkeyActions += solution.solution()
        food_locations.remove(solution.state)
        eater_locations = solution.state
    print(f"Total nodes visited: {totalCounter}")
    return monkeyActions