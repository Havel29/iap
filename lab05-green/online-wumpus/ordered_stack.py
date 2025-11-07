import numpy as np
from offline_search.search_algorithms import Frontier

class ordered_stack(Frontier):
    """The generic interface of a frontier for a search algorithm."""
    def __init__(self, elements):
            self.stack = elements

    def select_and_remove(self):
        return self.stack.pop(0)
    
    
    def order_frontier(self, currentDirection, currentPosition):
        move_directions = {'N': (0, 1), 'E': (1, 0), 'O': (-1, 0), 'S': (0, -1)}
        target_position = tuple(map(np.add, currentPosition, move_directions[currentDirection]))
        orderedNeighbor = [neighborCell for neighborCell in self.stack if neighborCell == target_position]
        if orderedNeighbor:
            self.stack.remove(orderedNeighbor[0])
        self.stack = orderedNeighbor + self.stack 

    def contains(self, node):
        return node in self.stack
        #return is_in(node, self.stack)

    def is_empty(self):
        return self.stack == []

    def add_all(self, localSafeCells, visitedCells, currentDirection, currentPosition):
        for locCell in localSafeCells:
            if(locCell not in self.stack and locCell not in visitedCells):
                self.stack=[(locCell[0], locCell[1])] + self.stack
         
        self.order_frontier(currentDirection, currentPosition)

    def get_element(self,index):
        return self.stack[index]
    
    def remove(self, obj):
        self.stack.remove(obj)

    def __repr__(self):
        return str(self.stack)