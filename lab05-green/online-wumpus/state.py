import numpy as np
from ordered_stack import *
from probabilistic_reasoner import Probabilistic_reasoner
from offline_search.A_star_problem import offline_search
from sat import getSafeAndUnsafeCells  

# State class
# Class that keeps track of the information about the current state of the world and consecutively manages the actions to be executed by the agent 
# according to the percepts 
class State:
    def __init__(self, currentPosition, currentDirection, currentDimension, breeze_cells, stench_cells, visitedCells, safeCells,  unsafeCells, riskyAgent):
        self.currentPosition = currentPosition  # store the current position of the hunter
        self.currentDirection = currentDirection # store the current direction of the hunter
        self.currentDimension = currentDimension # keeps track the dimension of the world explored so far
        self.breeze_cells = breeze_cells # store the position where breeze is percepted 
        self.stench_cells = stench_cells # store the position where stench is percepted 
        self.visitedCells = visitedCells # keeps track of the visited cells so far
        self.safeCells = ordered_stack(safeCells)
        self.unsafeCells = ordered_stack(unsafeCells) # keeps track of the potentially unsafe cells calculated by the sat solver
        self.foundGoal = False
        self.takenGoal = False
        self.isBacktracking=False
        self.mapBoundReached=False  
        self.hasShot = False
        self.riskyAgent = riskyAgent
         
    #Function that update the state variable according to percepts     
    def updateState(self, perceptString):
        perceptString=perceptString.replace(' ', '')
        percepts = perceptString.split(',')  
        if "Bump" in percepts:
            self.update_after_bump()
        if "Glitter" in percepts:
            self.foundGoal = True
        if "Stench" in percepts:
            if self.currentPosition not in self.stench_cells:
                    self.stench_cells.append((self.currentPosition[0],self.currentPosition[1]))
        if "Scream" in percepts: 
            self.stench_cells = [] # Remove all stench cells since wumpus has been killed
        if "Breeze" in percepts:
            if self.currentPosition not in self.breeze_cells :
                self.breeze_cells.append((self.currentPosition[0],self.currentPosition[1]))
        
    
    def rotateLeft(self):
        directions = ["N", "E", "S", "O"]
        return directions[(directions.index(self.currentDirection) - 1) % len(directions)]
    
    def rotateRight(self):
        directions = ["N", "E", "S", "O"]
        return directions[(directions.index(self.currentDirection) + 1) % len(directions)]

    def moveForward(self):
        direction_map = {
            "N": (0, 1),
            "S": (0, -1),
            "E": (1, 0),
            "O": (-1, 0)
        }
        newCoords = tuple(map(np.add, self.currentPosition, direction_map[self.currentDirection]))
        return newCoords
 
    # Given the current position and direction calculate the action needed to reach the destination cell
    def getActionTowards(self, cell, actions):  
        if self.moveForward() == cell:
            self.visitedCells.append((cell[0],cell[1]))
            return actions["MOVE"]
        self.currentDirection = self.rotateLeft()
        if (self.moveForward() == cell):
            self.currentDirection = self.rotateRight()
            return actions["LEFT"]
        self.currentDirection = self.rotateRight() 
        return actions["RIGHT"] 

    #Update information of the current state after perfoming an action
    def updateStateBasedOnAction(self, action, actions):
        if (action == actions["MOVE"]): 
            direction_map = {
                "N": (0, 1),
                "S": (0, -1),
                "E": (1, 0),
                "O": (-1, 0)
            }
            self.currentPosition = tuple(map(np.add, self.currentPosition, direction_map[self.currentDirection]))
            if (not self.mapBoundReached and self.currentPosition[0]+1>self.currentDimension[0]):
                self.currentDimension = (self.currentPosition[0]+1, self.currentPosition[0]+1)
            elif (not self.mapBoundReached and self.currentPosition[1]+1>self.currentDimension[1]):
                self.currentDimension = (self.currentPosition[1]+1, self.currentPosition[1]+1)
        
        elif (action == actions["RIGHT"]):
            self.currentDirection = self.rotateRight()
        elif (action == actions["LEFT"]):
            self.currentDirection = self.rotateLeft()



    #Exstablish the logic of the action to be choosed 
    def chooseAction(self, actions):
            
        #Check if there is a goal in this location
        handleTakeGoal=self.handle_take_goal(actions)
        if(handleTakeGoal):
            return handleTakeGoal    
            

        #Exploit the sat solver to deduce the safe and unsafe cells by taking into consideration breeze and stench cells discovered so far
        if(not self.mapBoundReached):
            localSafeCells, localUnsafeCells, possibleWumpus = getSafeAndUnsafeCells(self.currentPosition, (self.currentDimension[0]+1,self.currentDimension[1]+1), self.breeze_cells, self.stench_cells, self.visitedCells)
        else:  
            localSafeCells, localUnsafeCells,possibleWumpus = getSafeAndUnsafeCells(self.currentPosition, self.currentDimension, self.breeze_cells, self.stench_cells, self.visitedCells)
        self.possibleWumpus=possibleWumpus
        for cell in localSafeCells:
            if cell in self.unsafeCells.stack:
                self.unsafeCells.stack.remove(cell) #if this additional knowledge makes an unsafe cell safe, then remove it from the unsafeCells list

        #Update safe cells stack       
        self.safeCells.add_all(localSafeCells, self.visitedCells,self.currentDirection, self.currentPosition)
        
        #Update unsafe cells stack
        self.unsafeCells.add_all(localUnsafeCells, self.visitedCells, self.currentDirection,self.currentPosition)
                
        #Check if it is possible to shoot in this position
        handleShoot=self.handle_shoot(actions)
        if(handleShoot):
            return handleShoot
             
        ##Decision process for next action
        chosenAction = None
        #If there are no safe cells locally
        if len(localSafeCells) == 0 : #the ones returned by the getSafeAndUnsafe

            #If there are no safe cells 
            if(self.safeCells.is_empty()):
                if self.unsafeCells.is_empty() or self.riskyAgent == False:
                    #If there are no more unsafe cells or the agent is not risky then exit
                    chosenAction=self.handle_backtracking((0,0),True,actions)
                else:
                    #If the agent is risky calculate best cell and move to it
                    chosenAction=self.move_to_risk_cell(actions)

            #If there are safe cells available move to it
            else: chosenAction=self.handle_backtracking(self.safeCells.get_element(0),False,actions) 
             
        else: 
            #Continue inspecting the grid
            chosenAction = self.getActionTowards(self.safeCells.get_element(0), actions)
            
            if chosenAction == actions["MOVE"]: #if you can move to the cell then pop is from the safeCells          
                self.safeCells.select_and_remove()
            self.isBacktracking=False 
            
        self.updateStateBasedOnAction(chosenAction, actions)        
        return chosenAction
    

    #Backtrack to a destination using the offline search strategy 
    def handle_backtracking(self,goal,isClimbing,actions):
        if(not self.isBacktracking):
            self.listOfActionToOrigin=offline_search(self.currentPosition,self.currentDirection,goal,self.visitedCells+self.safeCells.stack,actions,self.currentDimension)
            if(isClimbing):
                self.listOfActionToOrigin=self.listOfActionToOrigin+[actions["CLIMB"]]
            self.isBacktracking=True 
            return self.listOfActionToOrigin.pop(0)
        else:
            if(len(self.listOfActionToOrigin)==1):
                self.isBacktracking=False
            return self.listOfActionToOrigin.pop(0)
         
    #Take goal strategy    
    def handle_take_goal(self,actions):        
        if self.foundGoal: #if you're in the gold cell
            if not self.takenGoal: #take the gold if not taken yet 
                self.takenGoal = True                  
                return actions["GRAB"]             
            else: #otherwise if already taken go back to the start  
                return self.handle_backtracking((0,0),True,actions)
    
    #Shoot strategy
    def handle_shoot(self,actions):
        direction_map = {"N": (0, 1),"S": (0, -1),"E": (1, 0),"O": (-1, 0)}
        if self.currentPosition in self.stench_cells and self.hasShot == False:
            if(tuple(map(np.add, self.currentPosition, direction_map[self.currentDirection])) in self.possibleWumpus):
                self.hasShot = True 
                return actions["SHOOT"]
            self.currentDirection=self.rotateLeft()
            if(tuple(map(np.add, self.currentPosition, direction_map[self.currentDirection])) in self.possibleWumpus):
                return actions["LEFT"]
            self.currentDirection=self.rotateRight()
            self.currentDirection=self.rotateRight()
            #In this method we update the state right away because updateStateBasedOnAction will not be called
            return actions['RIGHT']       
        return None

    #Updates world state information after bump                 
    def update_after_bump(self):
        if self.currentDirection == "N" or self.currentDirection == "E":
            self.mapBoundReached=True
            direction_map = {"N": (0, -1),"S": (0, 1),"E": (-1, 0),"O": (1, 0)} 
            self.currentPosition = tuple(map(np.add, self.currentPosition, direction_map[self.currentDirection]))
            self.currentDimension=(self.currentDimension[0]-1,self.currentDimension[1]-1) 
            variableToUpdate=[self.safeCells.stack,self.visitedCells,self.unsafeCells.stack]
            self.safeCells.stack,self.visitedCells,self.unsafeCells.stack = [ [cell for cell in variable if cell[0] < self.currentDimension[0] and cell[1] < self.currentDimension[1]] for variable in variableToUpdate]
            
    #Exploits the probalistic framework in order to compute the best cell to furtherly explore the world
    def handle_risk(self):
        if self.currentPosition in self.unsafeCells.stack:
            self.unsafeCells.remove(self.currentPosition)
        searchBound = (self.currentDimension[0]+1,self.currentDimension[0]+1) if not self.mapBoundReached else self.currentDimension
        probReasoner=Probabilistic_reasoner([item for item in self.visitedCells if item not in self.breeze_cells], self.breeze_cells, [item for item in self.visitedCells if item not in self.stench_cells], self.stench_cells, self.unsafeCells.stack, searchBound)
        safest_cell = probReasoner.getSafestCell()
        return safest_cell
    
    #Function to construct the action needed to reach the risky cell predicted by the probabilistic framework
    def move_to_risk_cell(self, actions):
        neighbors = [(x, y) for x, y in [(self.currentPosition[0] - 1, self.currentPosition[1]), (self.currentPosition[0], self.currentPosition[1] - 1), (self.currentPosition[0], self.currentPosition[1] + 1), (self.currentPosition[0] + 1, self.currentPosition[1])]]
        destCell = self.handle_risk()     
        #If the risky cell is in a neighbors cell wrt to the position of the agent move to it
        if destCell in neighbors:
            return self.getActionTowards(destCell,actions)
        else:
            #Otherwise construct path to it
            visitedNeighbors = [(x, y) for x, y in [(destCell[0] - 1, destCell[1]), (destCell[0], destCell[1] - 1), (destCell[0], destCell[1] + 1), (destCell[0] + 1, destCell[1])] if (x,y) in self.visitedCells]
            return self.handle_backtracking(visitedNeighbors[0],False,actions) 