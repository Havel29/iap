from search_problem import *


class Frontier:
    """The generic interface of a frontier for a search algorithm."""
    def __init__(self, elements):
        raise NotImplementedError

    def select_and_remove(self):
        raise NotImplementedError

    def contains(self, node):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    def add_all(self, elements):
        raise NotImplementedError

    def add(self, element):
        raise NotImplementedError


class StackFrontier(Frontier):
    """Implements the frontier as a stack"""
    def __init__(self, elements):
        self.stack = elements

    def select_and_remove(self):
        return self.stack.pop()

    def contains(self, node):
        #return node in self.stack
        return is_in(node, self.stack)

    def is_empty(self):
        return self.stack == []

    def add_all(self, elements):
        self.stack += elements

    def add(self, element):
        self.stack.append(element)

    def __repr__(self):
        return str(self.stack)

class Priority_Queue(Frontier):
    """Implements the frontier as a priority queue ordered by path_cost"""
    def __init__(self, elements):
        self.stack = elements

    def select_and_remove(self):
        return self.stack.pop()
    
    def order_frontier(self):
        self.stack = sorted(self.stack, key=lambda x: x.path_cost, reverse=True)

    def contains(self, node):
        return node in self.stack
        #return is_in(node, self.stack)

    def is_empty(self):
        return self.stack == []

    def add_all(self, elements):
        self.stack += elements
        self.order_frontier()

    def add(self, element):
        self.stack.append(element)
        self.order_frontier()

    def __repr__(self):
        return str(self.stack)
    
def tree_search(problem, frontier):
    """
    Generic search algorithm, without loops detection. Frontier must already be initialized to problem.initial (the initial node)
    """
    while not frontier.is_empty():
        node = frontier.select_and_remove()
        if problem.goal_test(node.state):
            return node
        frontier.add_all(node.expand(problem))
    return None

def graph_search(problem, frontier):
    """
    A generic search algorithm, with loop detection. Frontier must already be initialized to problem.initial (the initial node)
    """
    explored_states = set()
    counter = 0
    while not frontier.is_empty():
        node = frontier.select_and_remove()
        counter += 1
        if problem.goal_test(node.state):
            return node, counter
        explored_states.add(node.state)
        if(hasattr(problem, 'depth') and node.depth==problem.depth):
            continue
        for n in node.expand(problem): 
            if (n.state not in explored_states) and (not frontier.contains(n)):
                frontier.add(n)
    return None, counter

def dfs(problem):
    """A depth-first implementation (with loop detection)"""
    return graph_search(problem, StackFrontier([Node(problem.initial)]))