## Assignment 03 - Group Green
### Boscarato Luca 20154 - Tarolli Devid - 20758

### Exercise 1a and 1b
In this exercise we provide the results of the execution of the two planning problems 15Puzzle and 15Puzzle with Weights.

| Planning_problem | pddl_algorithm | heuristic | time | number of expanded states | number of generated states |
|------------------|----------------|-----------|------|---------------------------|----------------------------|
|  15-Puzzle | gready best first | ff() |   0.174912s   | 2753 | 8807  |
|  15-Puzzle | gready best first | add() |  0.145129s   | 1443 | 5307  |
|  15-Puzzle | gready best first | blind() |   0.174912s   |2753 | 8807 |
|  15-Puzzle Weight | gready best first | ff() |   0.194827s   | 3550 | 11106  |
|  15-Puzzle Weight | gready best first | add() |  0.340269s   | 6059 | 21551  |
|  15-Puzzle Weight | gready best first | blind() |   0.174912s   |2753 | 8807 |

From the statistics we can see that the costs in weight01 requires more computation in term of resourches and also in term of number of expanded and generated states. This can be expected since the algorithm is required to minimize the total cost given by each action.
In addition, from the statistics it can be evinced that the blind method performs not effectively since it explored more paths. While it seems that for both the problems additive heuristic generate less nodes in comparison with the FF heuristic. While for the simplest version of puzzle the additive heuristic  expands less states than add(). On the other hand, for the puzzle version with weights the FF heurist expands the least number of states, giving a faster solution.


### Exercise 1c
In the following we provide a comparison of the results of the *Glued 15-Glued* with the general puzzle problem and the weighted puzzle problem. The FF heristic seem to be the best both in number of expanded and generated states. Furthermore, we can see that by if a puzzle cannot be moved the number of actions needed to solve the problem increase significantly in comparison with a standard problem.

| Planning_problem | pddl_algorithm | heuristic | time | number of expanded states | number of generated states |
|------------------|----------------|-----------|------|---------------------------|----------------------------|
|  Glued 15-Puzzle | gready best first | ff() |   5.74265s   | 229858 | 634659  |
|  Glued 15-Puzzle | gready best first | add() |  52.8779s   | 2005642 | 5926523  |
|  Glued 15-Puzzle | gready best first | blind() |   0.174912s   |2753 | 8807 |
|  15-Puzzle | gready best first | ff() |   0.174912s   | 2753 | 8807  |
|  15-Puzzle | gready best first | add() |  0.145129s   | 1443 | 5307  |
|  15-Puzzle | gready best first | blind() |   0.174912s   |2753 | 8807 |
|  15-Puzzle Weight | gready best first | ff() |   0.194827s   | 3550 | 11106  |
|  15-Puzzle Weight | gready best first | add() |  0.340269s   | 6059 | 21551  |
|  15-Puzzle Weight | gready best first | blind() |   0.174912s   |2753 | 8807 |

### Exercise 1d 
In the following we provide a comparison of the results of the *Glued 15-Cheat* with the general puzzle problem and the weighted puzzle problem. The FF heristic seem to be the best both in number of expanded and generated states. Furthermore, we can see that by giving the possibility of extracting a tile the number of actions reduces drastically.

| Planning_problem | pddl_algorithm | heuristic | time | number of expanded states | number of generated states |
|------------------|----------------|-----------|------|---------------------------|----------------------------|
|  Cheat 15-Puzzle | gready best first | ff() |   0.0593461   | 49 | 584  |
|  Cheat 15-Puzzle | gready best first | add() |  0.145129s   | 53 | 625  |
|  Cheat 15-Puzzle | gready best first | blind() |   0.174912s   |2753 | 8807 |
|  15-Puzzle | gready best first | ff() |   0.174912s   | 2753 | 8807  |
|  15-Puzzle | gready best first | add() |  0.145129s   | 1443 | 5307  |
|  15-Puzzle | gready best first | blind() |   0.174912s   |2753 | 8807 |
|  15-Puzzle Weight | gready best first | ff() |   0.194827s   | 3550 | 11106  |
|  15-Puzzle Weight | gready best first | add() |  0.340269s   | 6059 | 21551  |
|  15-Puzzle Weight | gready best first | blind() |   0.174912s   |2753 | 8807 |

## Exercise 2
In this section we provide results of the exercise 2.

| Planning_problem | pddl_algorithm | heuristic | time | number of expanded states | number of generated states | Plan cost |
|------------------|----------------|-----------|------|---------------------------|----------------------------| ----------|
|  Vampire p01| gready best first | ff() |   0.0120345   | 13 | 65  | 5 |
|  Vampire p02| gready best first | ff() |  0.012748   | 7 | 31  | 4|
|  Vampire p03| gready best first | ff() |   0.0130637   |22 | 113 | 8|
|  Vampire p04 | gready best first | ff() |   0.0124905   | 9 | 42  | 5|
|  Vampire p05 | gready best first | ff() |  0.0115752   | 6 | 26  | 5|
|  Vampire p06 | gready best first | ff() |   0.0170598   |11 | 101 | 9|
|  Vampire p07 | gready best first | ff() |   0.018873   | 29 | 281  | 12|
|  Vampire p08 | gready best first | ff() |  0.0177918   | 13 | 121  | 10|
|  Vampire p09 | gready best first | ff() |   0.0230559   |22 | 316 | 16|
|  Vampire p10 | gready best first | ff() |   0.0292592   |66 | 976 | 16|

Comparing plan cost results obtained from the given one we can say that the implemented planner perform accordingly.

 
## Exercise 3
This problem domain is based on the proposal provided by the reference (written in the readme file). In addition, it enables the hunter to store the orientation via the direction-north, direction-south, direction-east, direction-west predicates and consequently to perform the rotate left or right action. 
For establishing the adjecency of a pair of cells wrt a direction the predicates adj-north, adj-east, adj-west, adj-south are defined.
In addition, the domain specifies several move actions by taking into account the current direction of the hunter. So at each state the proper move action will be expanded according to the orientation of the hunter. Furthermore, also rotate-right and rotate-left actions are specified, which allow the hunter to rotate left or right respectively. Cost of actions are taken into consideration by the increase total-cost operation, the problem tries always to minimize the cost of the action.

This section provides statistics about the implemented solution for the wumpus problem. Note that the wumpus folder contain some  problem instances. The solution includes the actions available in the wumpus problem such as rotate left, rotate right, shoot, move and climb.



| Planning_problem | pddl_algorithm | heuristic | time | number of expanded states | number of generated states | Plan cost |
|------------------|----------------|-----------|------|---------------------------|----------------------------| ----------|
| Wumpus 01 | gready best first | ff() |   0.0201241   | 59 | 162  | 28 |
| Wumpus 01 | gready best first | add() |   0.0249567   | 78 | 229  | 28 |
| Wumpus 02 | gready best first | ff() |   0236391s   | 44 | 124  | 27 |
| Wumpus 02 | gready best first | add() |   0.0244387   | 120 | 355  | 27 |
| Wumpus 03 | gready best first | ff() |   0.0189825   | 37 | 101  | 22 |
| Wumpus 03 | gready best first | add() |   0.0189485   | 49 | 143  | 23 |
| Wumpus 04 | gready best first | ff() |   0236391s  | 2 | 1  | 1 |
| Wumpus 04 | gready best first | add() |   0.0244387   | 2 | 1  | 1 |

Note wumpus 04 problem is a test for the climb action in the case the problem in unsolvable. In general, we can see that also for this kind of problem the FF heuristic appears to be the best in term of efficiency.

## Execution
For the execution of the planner is possible to use the command :
~~
fast-downward domain_file.pddl problem_file.pddl --heuristic "h=heuristic_type()" --search "eager_greedy([h])"
~~




