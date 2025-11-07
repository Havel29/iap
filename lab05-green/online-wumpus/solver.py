#!/usr/bin/env python

# Examples demonstrating the use of the Wumpus package

import argparse
import textwrap
import random
import sys
from typing import Iterable, Union
import traceback

import wumpus as wws
from state import State
from gridworld import Agent, Percept, object_id, GridWorld

class OnlinePlayer:
    """A player for a given agent. It implements the play method which should
    return one of the actions for the agent or None to give up.
    """
    def __init__(self, name: str = None):
        """
        Initialise the name of the player if provided.
        """
        self._name = str(name) if name is not None else object_id(self)

    @property
    def name(self) -> str:
        """The name of the player or a default value based on its type and hash."""
        return self._name

    def start_episode(self):
        """Method called at the beginning of the episode."""
        pass

    def end_episode(self, outcome: int, alive: bool, success: bool):
        """Method called at the when an episode is completed with the outcome of the game and whether the agent was still alive and successfull.
        """
        pass

    def play(self, percept: Percept, actions: Iterable[Agent.Actions], reward: Union[int, None]) -> Agent.Actions:
        """Given a percept, which might differ according to the specific problem, and the list of valid actions, returns an action to play at the given turn or None to stop the episode. The reward is the one obtained in the previous action, on the first turn its value is None."""
        raise NotImplementedError



class UserPlayerSafe(wws.OnlinePlayer):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.state = State((0,0), 'N', (1,1), [], [], [(0,0)], [], [], False)

    """This player asks the user for the next move, if it's not ambiguous it accepts also commands initials and ignores the case."""
    def play(self, percept: Percept, actions: Iterable[Agent.Actions], reward: int) -> Agent.Actions:
        actions_dict = {a.name: a for a in actions}
        stringPercept = str(percept)
        self.state.updateState(stringPercept)
        chosenAction = self.state.chooseAction(actions_dict)
        return chosenAction            


class UserPlayerRisky(UserPlayerSafe):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.state = State((0,0), 'N', (1,1), [], [], [(0,0)], [], [], True)

     
                        
def classic(size: int = 0):
    """Play the classic version of the wumpus."""
    # create the world
    world = wws.WumpusWorld.classic(size=size if size > 3 else random.randint(4, 8))

    # Run a player without any knowledge about the world
    wws.run_episode(world, UserPlayerSafe())

def fixed_classic():
    WUMPUS_WORLD1 = '''
    {
        "id": "simple wumpus world",
        "size": [6,6],
        "hunters": [[0, 0]],
        "pits": [[5,1], [5,2],[4,3],[3,3],[2,3],[0,3],[2,5]],
        "wumpuses": [],
        "exits": [[0, 0]],
        "golds": [[5,4]],
        "blocks": []
    }
    ''' 
    world = wws.WumpusWorld.from_JSON(WUMPUS_WORLD1)
    wws.run_episode(world, UserPlayerSafe())

    
def main():
    """Demonstrate the use of the wumpus API on selected worlds"""
    classic()

    return 0


if __name__ == "__main__":
    sys.exit(main())
