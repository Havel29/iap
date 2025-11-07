import numpy as np
from search_problem import Problem
from search_algorithms import *

class Ucs_problem(Problem):
    def __init__(self,initial, goal, actions, list_of_blocks):
        super().__init__(initial,goal, actions, list_of_blocks)

    def path_cost(self, path_cost,state)->int:
        return path_cost+1

def eat_banana(eater_locations,food_locations,actions,list_of_blocks):
    firstNode=Node(eater_locations, parent=None, action=None)
    problem=Ucs_problem(firstNode,food_locations,actions,list_of_blocks)
    solution,counter=graph_search(problem,Priority_Queue([firstNode]))
    return solution,counter

def ucs_runner(eater_locations,food_locations,actions,list_of_blocks):
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