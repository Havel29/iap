import itertools
import sys
import networkx as nx

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
class Probabilistic_reasoner:
    
    def __init__(self, not_breeze_cells, breeze_cells, not_stench_cells, stench_cells, query_cells, dimension) -> None:
        self.dimension=dimension
        self.not_breeze_cells = not_breeze_cells
        self.breeze_cells=breeze_cells
        self.not_stench_cells = not_stench_cells
        self.stench_cells = stench_cells
        self.query_cells=query_cells
        self.set_b_cpds()
        self.set_s_cpds()
        self.set_p_cdps()
        self.set_w_cdps()

    def cpd_values(self, bool_fn, arity):
        def bool_to_prob(*args) -> bool:
            return (1.0, 0.0) if bool_fn(*args) else (0.0, 1.0)

        return tuple(zip(*[bool_to_prob(*ps) for ps in itertools.product((True, False), repeat=arity)]))

    def set_p_cdps(self):
        self.p_cpds = {}
        for i in range(self.dimension[0]):
            for j in range(self.dimension[0]):
                self.p_cpds[(i, j)] = TabularCPD(
                    variable=f'P{i}{j}', variable_card=2, 
                    values=[[0.2], [0.8]], 
                    state_names={f'P{i}{j}': [True, False]})
                
    def set_w_cdps(self):
        self.w_cpds = {}
        number_cells = self.dimension[0] * self.dimension[0]
        w_prob = 1/number_cells
        for i in range(self.dimension[0]):
            for j in range(self.dimension[0]):
                self.w_cpds[(i, j)] = TabularCPD(
                    variable=f'W{i}{j}', variable_card=2, 
                    values=[[w_prob], [1-w_prob]], 
                    state_names={f'W{i}{j}': [True, False]})
 
    def pit_cpd(self, name, evidence, bool_fn):
        return TabularCPD(
            variable=name, variable_card=2,
            values=self.cpd_values(bool_fn, len(evidence)),
            evidence=evidence, evidence_card=[2] * len(evidence),
            state_names={n: [True, False] for n in [name] + evidence}
        )


    def wumpus_cpd(self, name, evidence, bool_fn):
        return TabularCPD(
            variable=name, variable_card=2,
            values=self.cpd_values(bool_fn, len(evidence)),
            evidence=evidence, evidence_card=[2] * len(evidence),
            state_names={n: [True, False] for n in [name] + evidence}
        )
    
    def set_b_cpds(self):         
        self.b_cpds={}
        grid_size = self.dimension[0]

        for i in range(grid_size):
            for j in range(grid_size):
                adjacent_cells = []
                if i > 0:
                    adjacent_cells.append(f'P{i-1}{j}')
                if i < grid_size - 1:
                    adjacent_cells.append(f'P{i+1}{j}')
                if j > 0:
                    adjacent_cells.append(f'P{i}{j-1}')
                if j < grid_size - 1:
                    adjacent_cells.append(f'P{i}{j+1}')
                b_val = f'B{i}{j}'
                if len(adjacent_cells) > 0:
                    if (i, j) == (0, 0):
                        self.b_cpds[(i, j)] = self.pit_cpd(b_val, adjacent_cells, lambda *args: any(args))
                    elif (i, j) == (0, grid_size - 1):
                        self.b_cpds[(i, j)] = self.pit_cpd(b_val, adjacent_cells, lambda *args: any(args))
                    elif (i, j) == (grid_size - 1, 0):
                        self.b_cpds[(i, j)] = self.pit_cpd(b_val, adjacent_cells, lambda *args: any(args))
                    elif (i, j) == (grid_size - 1, grid_size - 1):
                        self.b_cpds[(i, j)] = self.pit_cpd(b_val, adjacent_cells, lambda *args: any(args))
                    else:
                        self.b_cpds[(i, j)] = self.pit_cpd(b_val, adjacent_cells, lambda *args: any(args))

        return self.b_cpds

    def set_s_cpds(self):         
        self.s_cpds={}
        grid_size = self.dimension[0]

        for i in range(grid_size):
            for j in range(grid_size):
                adjacent_cells = []
                if i > 0:
                    adjacent_cells.append(f'W{i-1}{j}')
                if i < grid_size - 1:
                    adjacent_cells.append(f'W{i+1}{j}')
                if j > 0:
                    adjacent_cells.append(f'W{i}{j-1}')
                if j < grid_size - 1:
                    adjacent_cells.append(f'W{i}{j+1}')
                s_val = f'S{i}{j}'
                if len(adjacent_cells) > 0:
                    if (i, j) == (0, 0):
                        self.s_cpds[(i, j)] = self.wumpus_cpd(s_val, adjacent_cells, lambda *args: any(args))
                    elif (i, j) == (0, grid_size - 1):
                        self.s_cpds[(i, j)] = self.wumpus_cpd(s_val, adjacent_cells, lambda *args: any(args))
                    elif (i, j) == (grid_size - 1, 0):
                        self.s_cpds[(i, j)] = self.wumpus_cpd(s_val, adjacent_cells, lambda *args: any(args))
                    elif (i, j) == (grid_size - 1, grid_size - 1):
                        self.s_cpds[(i, j)] = self.wumpus_cpd(s_val, adjacent_cells, lambda *args: any(args))
                    else:
                        self.s_cpds[(i, j)] = self.wumpus_cpd(s_val, adjacent_cells, lambda *args: any(args))
        return self.s_cpds



    def computeEvicence(self):
        evidence = {}
        for i in range(self.dimension[0]):
            for j in range(self.dimension[0]):
                if (i,j) in self.breeze_cells:
                    evidence[f"B{i}{j}"] = True
                elif (i,j) in self.not_breeze_cells:
                    evidence[f"B{i}{j}"] = False
                if (i,j) in self.stench_cells:
                    evidence[f"S{i}{j}"] = True
                elif (i,j) in self.not_stench_cells:
                    evidence[f"S{i}{j}"] = False
        return evidence

    def getQueryCells(self):
        queryCells = []
        for x,y in self.query_cells:
            queryCells.append(f"P{x}{y}")
            queryCells.append(f"W{x}{y}")
        return tuple(queryCells)
    
    def getSafestCell(self):

        exp_model = BayesianNetwork()

        evidence=self.computeEvicence()
        for b in self.b_cpds.values():
            for e in b.get_evidence():
                #print("Adding edge:", e, b.variable) 
                exp_model.add_edge(e, b.variable)
        for s in self.s_cpds.values():
            for e in s.get_evidence():
                #print("Adding edge:", e, s.variable) 
                exp_model.add_edge(e, s.variable)
                
        exp_model.add_nodes_from([p.variable for p in self.p_cpds.values()]) 
        exp_model.add_nodes_from([w.variable for w in self.w_cpds.values()])  
                
        exp_model.add_cpds(*self.b_cpds.values())
        exp_model.add_cpds(*self.p_cpds.values())
        exp_model.add_cpds(*self.s_cpds.values())
        exp_model.add_cpds(*self.w_cpds.values())
  
        assert exp_model.check_model()

        exp_infer = VariableElimination(exp_model)
         
        query_probabilities = {}

        for v in self.getQueryCells():
            query_result = exp_infer.query([v], evidence=evidence, show_progress=False)
            
            query_probabilities[v] = query_result.values[0]  # Probability of True

        # Find the cell with the lowest probability of being True 
        max_probabilities = {}

        # Iterate through the keys in the query_probabilities dictionary
        for key in query_probabilities:
            # Extract the digits and the prefix (P or W) from the key
            digits = key[1:]
            prefix = key[0]

            # Construct the key for the output dictionary (TXX)
            output_key = 'T' + digits

            # If the output key doesn't exist in the max_probabilities dictionary
            # or if the value for the current key is greater than the existing value, update it
            if output_key not in max_probabilities or query_probabilities[key] > max_probabilities[output_key]:
                max_probabilities[output_key] = query_probabilities[key]        
    
        safest_cell = min(max_probabilities, key=max_probabilities.get) 
        return (int(safest_cell[1]),int(safest_cell[2]))

def main():
    #Example world
    breeze_cells = [(0,0)]
    not_breeze_cells=[(1,1),(1,2)]
    dimension = (5,5)
    query_cells = [(1,3),(2,2),(3,1)]
    prob = Probabilistic_reasoner(not_breeze_cells, breeze_cells, query_cells, dimension)
    prob.getSafestCell()
    return 0


if __name__ == "__main__":
    sys.exit(main())