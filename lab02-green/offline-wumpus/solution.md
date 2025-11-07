# Solution Assignment 02

### Group Green: Boscarato Luca - Tarolli Devid

### Implementation

This section contains the description of the code. The implementation is based on the given template for a generic search problem and adapted in order to accomplish the task of the assignment

#### The Frontier class hierarchy

The generic class `Frontier` describes the structure of a frontier/fringe of a search problem. It puts at disposal typical method such as ``select_and_remove`` and `is_empty`, including method for adding a node. According to the search algorithm it can act as a stack or a priority queue. In this sense, the class `StackFrontier` implements the frontier as a stack. Namely, the `select_and_remove` method returns always the last element added and removes it from the frontier. Also a concrete implementation of the generic method such as is_empty, add, add_all is provided. On the other hand, in this assignment we exploit the properties of the `Priority_Queue` since we deal with an informed search problem.  The priority queue implementation orders the frontier w.r.t. an ordering function. Every time a new object is added, it is ordered according to the *path_cost* attribute of the stored nodes. Consequently, for an A* problem it will return the node for which the *f(n)* function is lower.

#### The Graph search function

Additionally, the `graph_search` function (in *search-algorithms.py*) implements the common logic of a search algorithm. That is, select and remove a node from the frontier ordered according to the search problem, check if the node is a goal, if yes then the search procedure terminates, otherwise expand the current node and store its children. Since we are working with graphs, the code includes loop detection. The iterative procedure proceeds until no other element can be expanded. Note the presence of a counter for evaluation purpose.

#### The Problem hierarchy

The abstract `Problem` class represents a formal problem. It stores information about the *initial position* of the agent, the *goal* positions, the *list_of_blocks* representing pits and the *available_actions* for the hunter. The `actions` function implementation is demanded to the subclasses. Further, the `goal_test` function checks whether the current node position is a goal. The `path_cost` default implementation return always 1, which is redefined for the A* problem. While the `is_valid` function verifies if a position given is valid, that if it is within the matrix and if the position is not a pit.

##### The A_Star_Problem class

The `A_Star_Problem` class is an extension of the generic `Problem` class. It defines the `actions` function which calculate the expansion of a given node. In particular, it calculates the neighbor coordinates and the actions that the hunter should perform for reaching that neighbor. If the neighbor is a wumpus the actions needed include the shoot. (Whether to take this action is upon the heuristic).

Additionally, the class defines the `path_cost` method according to the f(n) function, where n is the current node. The formula of A* is *f(n) = g(n) + h(n)*. In this solution, *g(n)* is calculated as the cost for the path so far additioned to the cost for reaching the next node n. This is calculated by taking the number of action (left, right, move and eventually shot) needed by the hunter to reach the next node n. If the next node n is a location of the wumpus, add the cost of killing it (10pt) to the cost function. Then we sum this results with the heurist function cost *h(n)* which estimates the cost from the node n to the goal.
Hence, the next node selected by the frontier will be that one with the least cost, deciding if the wumpus should be killed or bypassed. Additionally, by adding the cost of actions (left, right, move) in f(n), the path decision process considers also the cost of moving and rotating the agent, which in some cases makes the research more performant. (This can be activated or disactivated for the evaluation of the performances)

This function *f(n)* is admissible since it is an under-estimation of the actual cost for reaching a goal and path costs are always greather than zero. This is the case since the heuristic function, i.e. the manhattan distance and euclidean distance, are admissible and the costant we sum are the cost of each action taken. (The cost of an action is 1 for left, right, move and 10 for shooting).

The `A_star_runner` function runs the search procedure in a more generic way than expected by the problem instructions. Namely, it is assumed that more than one wumpuses and gold can be assigned in the problem. (Yet 1 shot available). The program tries to collect as much gold as possible, even if in some cases is not capable to collect all ones. The A* runner runs problem since no other goal are found. Since the search is informed at each iteration the goal node of the problem is optimized w.r.t. the actual position of the agent (by setting the goal node as the node with minimum distance from the agent). For the return to the base yet another problem is istantiated in order to find the most efficient path.

### Evaluation
Here we provide an evaluation of the algorithm based on three sample problem. 

| search_problem | search_algorithm    | visited_nodes  | Reward |
| -------------- | ------------------- | -------------  | ------ |
| World 1        | A* - Manhattan      | 263             | 962      |
| World 1        | A* - Manhattan Path Cost Opt     | 274             | 962      |
| World 1        | A* - Euclidean      | 275             | 962      |
| World 1        | A* - Euclidean Path Cost Opt    | 288             | 962      |
| World 2        | A* - Manhattan      | 127             | 976      |
| World 2        | A* - Manhattan Path Cost Opt     | 162             | 976      |
| World 2        | A* - Euclidean      | 172             | 973      |
| World 2        | A* - Euclidean Path Cost Opt    | 208             | 976      |
| World 3        | A* - Manhattan      | 66             | 975      |
| World 3        | A* - Manhattan Path Cost Opt     | 69             | 975      |
| World 3        | A* - Euclidean      | 77             | 975      |
| World 3        | A* - Euclidean Path Cost Opt    | 83             | 975      |

From the data above we can conclude that generally the manhattan heuristic performs better than the euclidean since we are working with a grid world. The action cost optimization, on the other hand, may require more node to be visited.

### Run the algorithm

The following commands can be executed to run the algorithm, enabling or disabling path cost optimization (taking into account the agent's movement/rotation costs) and modifying the heuristic function:

```
gridrunner --world WumpusWorld --entry solver:AStarManhattanPlayer --horizon=1000

gridrunner --world WumpusWorld --entry solver:AStarManhattanActionOptPlayer --horizon=1000

gridrunner --world WumpusWorld --entry solver:AStarEuclideanPlayer --horizon=1000

gridrunner --world WumpusWorld --entry solver:AStarEuclideanActionOptPlayer --horizon=1000
```
