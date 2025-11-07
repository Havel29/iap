import numpy as np


def is_in(elt, seq):  # Utility function
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)


class Problem:
    """The abstract class for a formal problem. You should subclass this and implement the methods and
    actions and result, and possibly __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal, available_actions, list_of_blocks):
        self.initial = initial
        self.goal = goal
        self.list_of_blocks=list_of_blocks
        self.available_actions=available_actions
        

    def actions(self, node):
        available_neighbors=[]
        for action in self.available_actions:
            neighbor=tuple(map(np.add, node.state, action.value))
            if self.is_valid(neighbor):
                available_neighbors.append({'neighbor':neighbor,'action':action})
        return available_neighbors

    def result(self, state, action): # The result of applying an action
        return action
    
    def goal_test(self, state): 
        return state in self.goal

    def path_cost(self, path_cost,state)->int:
        return 1
    
    def is_valid(self,new_pos): 
        return (new_pos not in self.list_of_blocks and
        new_pos[0]<=15 and new_pos[0]>=0 
        and new_pos[1]>=0 and new_pos[1]<=15)
    
    


class Node:
    """
    A node in the search tree
    """
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action # action from parent to this node
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return '(state:'+str(self.state)+" action: "+str(self.action)+" depth: "+str(self.depth)+' Path_cost: '+str(self.path_cost)+")"

    def __lt__(self, node):
        return self.path_cost < node.path_cost

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action['neighbor'])
        next_node = Node(state=next_state, parent=self, action=action['action'], 
                         path_cost=problem.path_cost(self.path_cost,next_state))
        return next_node

    # Returns a set of actions
    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)