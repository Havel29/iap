#!/usr/bin/env python

# Examples demonstrating the use of the Wumpus package

import argparse
import random
import sys
from typing import Iterable

import wumpus as wws
from A_star_problem import A_star_runner
from utility_functions import manhattan_distance, euclidean_distance


class GeneralSearchPlayer(wws.OfflinePlayer):
    """Offline player demonstrating the use of the start episode method to inspect the world."""

    def start_episode(self, world: wws.WumpusWorld) -> Iterable[wws.Hunter.Actions]:
        """Print the description of the world before starting."""

        world_info = {k: [] for k in ('Hunter', 'Pits', 'Wumpus', 'Gold', 'Exits')}
        world_info['Size'] = (world.size.x, world.size.y)
        world_info['Blocks'] = [(c.x, c.y) for c in world.blocks]

        for obj in world.objects:
            if isinstance(obj, wws.Hunter):
                world_info['Hunter'].append((obj.location.x, obj.location.y))
                all_actions = list(obj.Actions)
            elif isinstance(obj, wws.Pit):
                world_info['Pits'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Wumpus):
                world_info['Wumpus'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Exit):
                world_info['Exits'].append((obj.location.x, obj.location.y))
            elif isinstance(obj, wws.Gold):
                world_info['Gold'].append((obj.location.x, obj.location.y))

        print('World details:')
        for k in ('Size', 'Pits', 'Wumpus', 'Gold', 'Exits', 'Blocks'):
            print('  {}: {}'.format(k, world_info.get(k, None)))
        print(world_info)
        solution = self.search(world_info['Hunter'][0], world_info['Gold'], all_actions, world_info['Pits'], world_info['Wumpus'], world_info['Size'])
        return solution



class AStarManhattanPlayer(GeneralSearchPlayer):
    def search(self, eater_location, gold_locations, all_actions, block_locations, wumpus, size):
        return A_star_runner(eater_location, gold_locations, all_actions, block_locations,manhattan_distance, wumpus, size, False)

class AStarManhattanActionOptPlayer(GeneralSearchPlayer):
    def search(self, eater_location, gold_locations, all_actions, block_locations, wumpus, size):
        return A_star_runner(eater_location, gold_locations, all_actions, block_locations,manhattan_distance, wumpus, size, True)


class AStarEuclideanPlayer(GeneralSearchPlayer):
    def search(self, eater_location, gold_locations, all_actions, block_locations, wumpus, size):
        return A_star_runner(eater_location, gold_locations, all_actions, block_locations,euclidean_distance, wumpus, size, False)

class AStarEuclideanActionOptPlayer(GeneralSearchPlayer):
    def search(self, eater_location, gold_locations, all_actions, block_locations, wumpus, size):
        return A_star_runner(eater_location, gold_locations, all_actions, block_locations,euclidean_distance, wumpus, size, True)


WUMPUS_WORLD1 = '''
    {
        "id": "simple wumpus world",
        "size": [7, 7],
        "hunters": [[0, 0]],
        "pits": [[0,2],[1, 2], [2, 2], [3, 2], [2, 0], [5,0], [5,5], [5,6], [3,5], [3,6]],
        "wumpuses": [[4,1], [4,4]],
        "exits": [[0, 0]],
        "golds": [[4,4]],
        "blocks": []
    }
'''


WUMPUS_WORLD3 = '''
    {
        "id": "wumpus-v0",
        "size": [5,5],
        "hunters": [[0, 0, "N"]],
        "pits": [[1,1],[2,1],[3,1],[4,0],[3,2]],
        "wumpuses": [[2,3],[3,3],[4,3],[1,2]],
        "golds": [[4,1],[2,2]]
    }
'''

WUMPUS_WORLD2 = '''
    {
        "id": "simple wumpus world",
        "size": [7, 7],
        "hunters": [[0, 0]],
        "pits": [[4, 0], [6, 2], [2,2],  [4, 4], [3, 5], [4, 6], [5, 6]],
        "wumpuses": [[5, 1]],
        "exits": [[0, 0]],
        "golds": [[6, 3]],
        "blocks": []
    }
'''



def fixed_offline(world_json: str = WUMPUS_WORLD1):
    """Play on a given world described in JSON format."""
    world = wws.WumpusWorld.from_JSON(world_json)
    wws.run_episode(world, AStarManhattanActionOptPlayer())

def classic_offline(size: int = 0):
    """Play the classic version of the wumpus with a player knowing the world and the agent."""
    # create the world
    world = wws.WumpusWorld.classic(size=size if size > 3 else random.randint(4, 8))
 
    # Run a player with knowledge about the world
    wws.run_episode(world, AStarManhattanActionOptPlayer())


def main():
    """Demonstrate the use of the wumpus API on selected worlds"""
    classic_offline()

    return 0


if __name__ == "__main__":
    sys.exit(main())
