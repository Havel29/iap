#!/usr/bin/env python

"""
Examples of the use of the EaterWorld class
"""

from operator import add
import random
from typing import Iterable
import sys
from pathlib import Path

from Ucs_problem import ucs_runner

from A_star_problem import A_star_runner, manhattan_distance, euclidean_distance

from wumpus import OfflinePlayer, run_episode, Eater, EaterWorld, Food
from Dfs_problem import dfs_runner, iterative_deepening_runner

class GeneralSearchPlayer(OfflinePlayer):
    def _say(self, text: str):
        print(self.name + ' says: ' + text)

    def start_episode(self, world: EaterWorld) -> Iterable[Eater.Actions]:
        self.reward = 0
        self._say('Episode starting for player {}'.format(self.name))

        food_locations, eater_location, all_actions, block_locations = self.inspect_world(world)

        self._say('Actions : {}'.format(all_actions))
        self._say('World size: {}x{}'.format(world.size.x, world.size.y))
        self._say('Eater agent in {}'.format(eater_location))
        self._say('Food in {}'.format(sorted(food_locations)))
        self._say('Blocks in {}'.format(block_locations))
        self._say('Available actions: {}'.format({a.name: a.value for a in all_actions}))

        solution = self.search(eater_location, food_locations, all_actions, block_locations)
        return solution

    def end_episode(self, outcome: int, alive: bool, success: bool):
        self._say('Episode completed, my reward is {}'.format(outcome))

    def inspect_world(self, world):
        food_locations = []
        eater_location = None
        for o in world.objects:
            if isinstance(o, Eater):
                eater_location = (o.location.x, o.location.y)
                all_actions = list(o.Actions)
            elif isinstance(o, Food):
                food_locations.append((o.location.x, o.location.y))
        block_locations = sorted((bl.x, bl.y) for bl in world.blocks)
        return food_locations, eater_location, all_actions, block_locations

    def search():
        raise NotImplementedError

class UCSPlayer(GeneralSearchPlayer):
    def search(self, eater_location, food_locations, all_actions, block_locations):
        return ucs_runner(eater_location, food_locations, all_actions, block_locations)

class AStarManhattanPlayer(GeneralSearchPlayer):
    def search(self, eater_location, food_locations, all_actions, block_locations):
        return A_star_runner(eater_location, food_locations, all_actions, block_locations,manhattan_distance)

class AStarEuclideanPlayer(GeneralSearchPlayer):
    def search(self, eater_location, food_locations, all_actions, block_locations):
        return A_star_runner(eater_location, food_locations, all_actions, block_locations,euclidean_distance)

class IterativeDeepeningPlayer(GeneralSearchPlayer):
    def search(self, eater_location, food_locations, all_actions, block_locations):
        return iterative_deepening_runner(eater_location, food_locations, all_actions, block_locations)

#gridrunner --world EaterWorld --entry solver:AStarEuclideanPlayer --horizon 200 worlds/eater-world_5.json
#gridrunner --world EaterWorld --entry solver:AStarManhattanPlayer --horizon 200 worlds/eater-world_5.json
#gridrunner --world EaterWorld --entry solver:IterativeDeepeningPlayer --horizon 200 worlds/eater-world_5.json
#gridrunner --world EaterWorld --entry solver:UCSPlayer --horizon 200 worlds/eater-world_5.json


MAP_STR = """
################
#    #    #    #
#    #    #    #
#    #         #
#    #    #    #
###           ##
"""


def main(*args):
    """
    Play a random EaterWorld episode using the default player
    """

    player_class = args[0]
    print(MAP_STR)
    world = None
    with open('./worlds/eater-world_4.json') as fp:
        world = EaterWorld.from_JSON(fp)
    print(world)

    player = player_class('Hungry.Monkey')

    run_episode(world, player, horizon=200)

    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
