from math import sqrt
import numpy as np
from search_problem import Problem
from search_algorithms import *

class A_star_problem(Problem):
    def __init__(self,initial, goal, actions, list_of_blocks, heuristic_function):
        self.heuristic_function=heuristic_function
        super().__init__(initial,goal, actions, list_of_blocks)

    def path_cost(self, path_cost, state)->int:
        #return 1+path_cost+manhattan_distance(state, self.goal[0])
        return 1+path_cost+self.heuristic_function(state, self.goal[0])

def manhattan_distance(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def euclidean_distance(pos1,pos2):
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    
def getClosestFood(eater_locations, food_locations, heuristic_function):
     return min(food_locations, key=lambda loc: heuristic_function(eater_locations, loc))

def eat_banana(eater_locations,food_locations,actions,list_of_blocks,heuristic_function):
    firstNode=Node(eater_locations, parent=None, action=None,path_cost=0)
    problem=A_star_problem(firstNode,[
        getClosestFood(eater_locations, food_locations, heuristic_function)
    ],actions,list_of_blocks, heuristic_function)
    solution, counter =graph_search(problem,Priority_Queue([firstNode]))
    return solution, counter

 

def A_star_runner(eater_locations,food_locations,actions,list_of_blocks,heuristic_function):
    monkeyActions = []
    totalCounter = 0
    while len(food_locations) > 0:
        solution, counter = eat_banana(eater_locations, food_locations, actions, list_of_blocks, heuristic_function)
        totalCounter += counter
        monkeyActions += solution.solution()
        food_locations.remove(solution.state)
        eater_locations = solution.state
    print(f"Total nodes visited: {totalCounter}")
    return monkeyActions