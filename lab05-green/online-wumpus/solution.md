# Solution of Assignment 05 
### Group Green: Boscarato Luca 20154 - Tarolli Devid 20758

### Description of the code
This section provides a description of the implemented code and strategy for solving the online wumpus problem.
The structure of the project is composed as follows:
    - **State** class: class deputated to take decision based on the current world information and the given percept 
    - **Sat** class: defines a sat solver in order to compute the safe and unsafe cells wrt the current world information
    - **Probabilistic_reasoner**: defines a bayesian network in order to compute risk probability of unsafe cells for the risky agent
    - **Offline wumpus package**: package of the offline wumpus project used for the moving the agent more effectively in situation when the world is known
    - **Solver** class: entry point of the program

#### State class
The state class describes the logic for the online wumpus problem. Keeps track of the information about the current state of the world and consecutively computes the actions to be executed by the agent by taking into consideration safe and unsafe cells deduced by the sat solver and probabilities of risky cells calculated by the bayesian network.
The core functions of such class are: 

- **updateState**: this function update the current world information according to percepts. In particular, if the percept is *bump* the *update_after_bump* function will set the grid dimension variable accordingly and checks the validity of cells present in the safe and unsafe cells. Additionally, if the percept is *glitter* it means that the goal is found and can be collected. The *choose_action* function will set the proper actions. If *stench* or *breeze* has been detected then we update the stench_cells and breeze_cells lists accordingly. While if there is a *scream* it means that the only wumpus present has been killed, hence there are no more stench cells.

- **getActionTowards**: function that given the current position and direction of the hunter calculates the action needed to reach the destination cell

- **handle_backtracking**: function that given the destination cell uses the offline wumpus package for calculating the best path to it according to *A**. It will compute and execute the list of action to reach it and eventually add the Grab action.

- **handle_risk**: function that exploits the probalistic framework in order to compute the best cell with lower risk to furtherly explore the world. It instantiates the *probabilistic_reasoner* class which constructs a bayesian network for calculating the probabilities of risk for the unsafe cells.

- **move_to_risk_cell**: function to construct the actions needed to reach the less risky cell computed by the probabilistic framework. Calls the handle_risk function to compute the risky cell to go to. 

- **chooseAction**: main method that describes the logic of the action to be choosen. It firstly, checks if there is a goal in the current location by means of the *handle_take_goal* helper method. If the goal has been found, calls the handle_backtracking function that computes the most effective path to climb out.

    Additionally, it checks if it convenient to shoot in this position. The *handle_shoot* function performs this operation if there is stench in the current position and orientates the wumpus in order to have an higher success of killing it. 

    Furthermore, we use the *sat solver* to deduce the local safe and unsafe cells by taking into consideration breeze and stench cells discovered so far. The project use a *deepth-first frontier* for both the safe and unsafe cells for deciding the next cell to go to.

    After the calculation of this cells we proceed to decide the next action to perform. Namely, if there are safe cells locally it continues to inspect the grid by taking the first element available from the frontier and compute the actions to reach it. However, if there are no safe cells locally we select the next cell from the safe_cells frontier and the agent goes to it. On the other hand, if there are no more safe cells, that is, if the safe_cells frontier is empty, then we decide accordingly to the kind of agent.
    The safe agent will climb out if there are no more safe cells available. The procedure will call the handle_backtracking method to compute the most effective path to reach the origin and climb out.
    Otherwise, the risky agent will move to the cell with lower risk (by calling the move_to_risk_cell function).  

#### Sat solver
This class constructs the z3 sat solver for the prediction of the safe and unsafe cells. It firstly defines boolean variables for stench, breeze, pits and wumpus cells and facts based on the current state of the world. Additionally, it specifies the constraints for determining the presence of pits and wumpus cells. Finally, the procedure let the z3 solver to compute the possible models for pits and wumpus positions and consequently returns the safe and unsafe cells.

#### Probabilistic Reasoner
This class defines the bayesian network used to calculate probabilities for risky cells, included the wumpus cells. This class implementation is based on the sample code provided by the instructor.

### Evaluation
In order to do the evaluation of the algorithm we use the *statistic.py* class which runs the safe agent for 40 times: the outcome is positive we gain generally 13421 points (average of 335.525).
On the other hand, the risky agent on 40 times loses 838 points (average of 20.95 lost per episode).

On the whole, it seems that the safe agent performs better than the risky agent since the loss of points when die occurs is high. The safe agent climbs out immediately when there are no more safe cells available, hence the loss of points is lower since only 1 pt for move is lost.  


### Run the algorithm

The following commands can be executed to run the algorithm, enabling or disabling the possibility to discover unsafe cells:

```
gridrunner --world WumpusWorld --entry solver:UserPlayerRisky --horizon=5000

gridrunner --world WumpusWorld --entry solver:UserPlayerSafe --horizon=5000 

```
