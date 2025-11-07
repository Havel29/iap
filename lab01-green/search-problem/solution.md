# Solution Assignment 01

### Group Green: Boscarato Luca - Tarolli Devid

### Implementation
This section contains the description of the code. The implementation is based on the given template for a generic search problem.

#### The Frontier class hierarchy
The generic class `Frontier` describes the structure of a frontier/fringe of a search problem. It puts at disposal typical method such as ``select_and_remove`` and `is_empty`, including method for adding a node. According to the search algorithm it can act as a stack or a priority queue. In this sense, the class `StackFrontier` implements the frontier as a stack. Namely, the `select_and_remove` method returns always the last element added and removes it from the frontier. Also a concrete implementation of the generic method such as is_empty, add, add_all is provided. On the other hand, the `Priority_Queue` class orders the frontier w.r.t. an ordering function. Every time a new object is added, it is ordered according to the *path_cost* attribute of the stored nodes. Consequently, in the context of a UCS problem the frontier will select the node with the least path_cost so far, while for a A* problem it will return the node for which the *f(n)* function is lower.

#### The Graph search function

Additionally, the `graph_search` function (in *search-algorithms.py*) implements the common logic of a search algorithm. That is, select and remove a node from the frontier ordered according to the search problem, check if the node is a goal, if yes then the search procedure terminates, otherwise expand the current node and store its children. Since we are working with graphs, the code includes loop detection. The iterative procedure proceeds until no other element can be expanded. Note the presence of a counter for evaluation purpose and the presence of a check for the depth of a node which is used by the iterative deepening approach.

#### The Problem hierarchy

The abstract `Problem` class represents a formal problem. It stores information about the *initial position* of the agent, the *goal* positions, the *list_of_blocks* representing boundaries and the *available_actions* for the agent at each position. The `actions` function receives as parameter a node and return its expansion, that is a list of available neighbors. Further, the `goal_test` function checks whether the current node position is a goal. The `path_cost` default implementation return always 1, which is true for a UCS problem.

##### The DFS_Problem class

Simple class that istantiates a problem by taking into consideration also the depth param. The `eat_banana` helper function runs a Dfs_problem with the depth attribute. Initially, the depth of a iterative deepening problem is zero. If a  solution is found the procedure stops. Otherwise, the depth increases countinuously until it reaches a treshold. Note that the graph_search stops when a solution is encountered. The `iterative_deepening_runner` function calls the function `eat_banana` until no other food is available. Namely, at each execution the food_location array, the eater_location are updated and the monkeys action are stored.

##### The UCS_Problem class

Similarly, the `UCS_Problem` class defines the path_cost method as the sum of the cost so far incresed by one unit. Furthermore, the `ucs_runner` function runs the search procedure until no other bananas are found.

##### The A_Star_Problem class

The `A_Star_Problem` class defines the `path_cost` method according to the f(n) function. It sums the cost so far plus the heuristic function cost that can be calculated by the manhattan or euclidean distance.
The `A_star_runner` function runs the search procedure until no other bananas are found. Note that since the search is informed at each iteration the goal node of the problem is optimized w.r.t. the actual position of the agent (by setting the goal node as the node with minimum distance from the agent).

### Evaluation

| search_problem | search_algorithm    | visited_nodes | memory_usage | running_time | Reward |
| -------------- | ------------------- | ------------- | ------------ | ------------ | ------ |
| World 1        | A* - Manhattan      | 24            | 30968        | 0.30         | 2      |
| World 1        | A* - Euclidean      | 35            | 34520        | 0.32         | 2      |
| World 1        | UCS                 | 35            | 30916        | 0.33         | 2      |
| World 1        | Iterative deepening | 36            | 30788        | 0.34         | 2      |
| World 2        | A* - Manhattan      | 44            | 31032        | 0.33         | -2     |
| World 2        | A* - Euclidean      | 44            | 33116        | 0.27         | -2     |
| World 2        | UCS                 | 68            | 30928        | 0.31         | -2     |
| World 2        | Iterative deepening | 56            | 31056        | 0.41         | -14    |
| World 3        | A* - Manhattan      | 62            | 31016        | 0.32         | 12     |
| World 3        | A* - Euclidean      | 62            | 32512        | 0.29         | 12     |
| World 3        | UCS                 | 81            | 30808        | 0.35         | 12     |
| World 3        | Iterative deepening | 69            | 31068        | 0.38         | 6      |
| World 4        | A* - Manhattan      | 253           | 31124        | 0.32         | -34    |
| World 4        | A* - Euclidean      | 258           | 33016        | 0.35         | -34    |
| World 4        | UCS                 | 345           | 31044        | 0.38         | -34    |
| World 4        | Iterative deepening | 163           | 31112        | 0.59         | -41    |
| World 5        | A* - Manhattan      | 482           | 31328        | 0.38         | 715    |
| World 5        | A* - Euclidean      | 631           | 33232        | 0.41         | 681    |
| World 5        | UCS                 | 668           | 31180        | 0.33         | 717    |
| World 5        | Iterative deepening | 458           | 31152        | 0.40         | 739    |

From the data above we can conclude that iterative deepening performs well only when the number of bananas in the world is high, otherwise informed search algorithms are better. The best one in this case (for a low number of bananas) is A* with the Manhattan Distance heuristic, as we could expect by looking at how the world is structured (in a grid format).


### Run the algorithm
In order to run the algorithm you can execute the `generate_report.sh` file which outputs a report including the results of the time command for inspecting the required system resources and the number of node visited by different algorithms.
Instead for executing a singular class run the command (where the solver param specifies the type of solver and the last param specifies the world):
~~~
gridrunner --world EaterWorld --entry solver:AStarEuclideanPlayer --horizon 200 worlds/eater-world_1.json

gridrunner --world EaterWorld --entry solver:AStarManhattanPlayer --horizon 200 worlds/eater-world_1.json

gridrunner --world EaterWorld --entry solver:IterativeDeepeningPlayer --horizon 200 worlds/eater-world_1.json

gridrunner --world EaterWorld --entry solver:UCSPlayer --horizon 200 worlds/eater-world_1.json 
~~~