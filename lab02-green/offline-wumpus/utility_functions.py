from math import sqrt


def manhattan_distance(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def euclidean_distance(pos1,pos2):
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    
def getClosestGold(eater_locations, gold_locations, heuristic_function):
     return min(gold_locations, key=lambda loc: heuristic_function(eater_locations, loc))
