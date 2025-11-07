import numpy as np

def is_in(elt, seq):  # Utility function
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)


class Problem:
    """The abstract class for a formal problem. You should subclass this and implement the methods and
    actions and result, and possibly __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal, available_actions, list_of_blocks, size):
        self.initial = initial
        self.goal = goal
        self.list_of_blocks=list_of_blocks
        self.available_actions=available_actions
        self.size = size
        
    def actions(self, node):
        raise NotImplementedError

    def result(self, state, action): # The result of applying an action
        return action
    
    def goal_test(self, state): 
        return state in self.goal

    def path_cost(self, path_cost,state)->int:
        return 1
    
    #Check if the neighbor generated is valid. That is, if it is in the matrix and if it is not in the position of a pit
    def is_valid(self,new_pos): 
        return (new_pos not in self.list_of_blocks and
        new_pos[0]<self.size[0] and new_pos[0]>=0 
        and new_pos[1]>=0 and new_pos[1]<self.size[1])

class Node:
    """
    A node in the search tree
    """
    def __init__(self, state, direction, killedWumpuses, parent=None, action=None, path_cost=0 ):
        self.state = state
        self.direction=direction
        self.parent = parent
        self.action = action # action from parent to this node
        self.path_cost = path_cost
        self.killedWumpuses = killedWumpuses

    def __repr__(self):
        return '(state:'+str(self.state)+" direction: "+str(self.direction)+" action: "+str(self.action)+' Path_cost: '+str(self.path_cost)+" - Killed Wumpuses: "+str(self.killedWumpuses)

    def __lt__(self, node):
        return self.path_cost < node.path_cost

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action['neighbor'])
        next_node = Node(state=next_state, 
                         direction=action['direction'], 
                         killedWumpuses=action['killedWumpuses'],
                         parent=self, 
                         action=action['action'], 
                         path_cost=problem.path_cost(self.path_cost,next_state, action['action'])
                        )

        return next_node

    # Returns a set of actions
    def solution(self):
        actions=[]
        for node in self.path()[1:]:
            actions+=node.action
        return actions

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state and self.direction == other.direction

    def __hash__(self):
        return hash((self.state,self.direction,self.killedWumpuses))