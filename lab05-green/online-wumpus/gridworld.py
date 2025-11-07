"""GridWorld implementation

This file implements the basics of a rectangular grid world, and the objects
that might populate it. Including a simple agent that can move in four directions.
"""

import collections
from dataclasses import dataclass
from enum import Enum
from inspect import cleandoc
import io
import json
import random
import sys
from typing import Set, NamedTuple, Iterable, Dict, Union, Any


def object_id(obj: Any, nbits: int = 32) -> str:
    """Build a string identifying the object using hashing anc class name. The object hash is reduced to the given number of bits nbits if it's greater than zero."""
    # hash_id = hash(obj)
    hash_id = (hash(obj) + (1 << nbits)) % (1 << nbits) if nbits else hash(obj)
    return '{}_{:x}'.format(type(obj).__name__, hash_id)


class Coordinate(NamedTuple):
    """Cartesian 2D coordinates."""
    x: int
    y: int


def coord(x: int, y: int, *args) -> Coordinate:
    """
    Return a Coordinates named tuple, first argument is horizontal and second vertical.

    Ignores additional arguments.
    """
    return Coordinate(x=x, y=y)


# Wide characters conversion
#   see <https://stackoverflow.com/a/16317693>

_TO_WIDE_TABLE = dict((i, chr(i + 0xfee0)) for i in range(0x21, 0x7f))
_TO_WIDE_TABLE.update({0x20: u'\u3000', 0x2D: u'\u2212'})  # space and minus


def ascii_to_wide(in_ascii: str) -> str:
    """Converts ASCII characters in the input string into their wide versions.

    Args:
        in_ascii (str): input string

    Returns:
        str: converted string
    """
    return in_ascii.translate(_TO_WIDE_TABLE)


class WorldObject(object):
    """An object, agent, or any other element that might be placed in a GridWorld."""
    def __init__(self):
        self._world: GridWorld = None

    def _setWorld(self, world: 'GridWorld'):
        self._world = world

    @property
    def location(self) -> Coordinate:
        """Return the location of the object in the world or None if it's not inside a world."""
        return self.world.location_of(self) if self.world is not None else None

    @property
    def world(self) -> 'GridWorld':
        """Return the world in which the object is or None if it's not inside a world."""
        return self._world

    @property
    def name(self) -> str:
        """Return the name of the object."""
        return object_id(self)

    def charSymbol(self) -> str:
        """Return the character for the object in the textual representation of the world."""
        raise NotImplementedError


class Actions(Enum):
    """The actions that an agent can perform."""
    pass


class Percept(object):
    """Agent perception of the environment."""
    pass


class Agent(WorldObject):
    """Is a special kind of world object that perform actions."""

    class Actions(Actions):
        """
        The actions of this agent.
        """
        pass

    class Percept(Percept):
        """
        The perception of this agent.
        """
        pass

    @classmethod
    def actions(cls) -> Iterable[Actions]:
        """Return the actions that the agent can execute as an iterable object."""
        return cls.Actions

    @property
    def reward(self) -> int:
        """The current accumulated reward"""
        raise NotImplementedError

    @property
    def isAlive(self):
        """Return true is the agent can still execute actions."""
        return True

    def percept(self) -> 'Agent.Percept':
        """Return the perception of the environment. None by default."""
        return None

    def do(self, action: 'Agent.Actions') -> int:
        """Execute an action and return the reward of the action."""
        raise NotImplementedError

    def suicide(self) -> int:
        """Kill the agent, returns the outcome of the action."""
        # I don't know how to die
        return 0

    def on_done(self):
        """Called when the episode terminate."""
        pass

    def success(self) -> bool:
        """Return true once the goal of the agent has been achieved."""
        return False


class GridWorldException(Exception):
    """Root of the exceptions raised by the GridWorld code."""
    pass


class OutOfBounds(GridWorldException):
    """Raised when an object is placed outside the bounds of the world."""
    pass


class Collision(GridWorldException):
    """Raised when an object cannot be placed because is colliding with another object or block."""
    pass


class GridWorld(object):

    def __init__(self, size: Coordinate, blocks: Iterable[Coordinate]):
        self._size = size
        self._blocks = set(blocks)
        self._objects: Dict[WorldObject, Coordinate] = {}
        self._location: Dict[Coordinate, Iterable[WorldObject]] = {}

    @classmethod
    def random(cls, map_desc: str=None, size: Coordinate=None, blocks: Iterable[Coordinate]=None, **kwargs):
        """Create a new world from a map description or from the given size and block positions.

        Args:
            map_desc (str, optional): map of the world. Defaults to None.
            size (Coordinate, optional): size of the world. Defaults to None.
            blocks (Iterable[Coordinate], optional): location of the blocks. Defaults to None (random placement).
        """

        if map_desc is not None:
            return cls.from_string(map_desc)
        if size is None:
            new_size = random.randint(4, 8)
            size = coord(new_size, new_size)
        if blocks is None:
            # randomly place blocks in the world
            blocks = set()
            occupy = int(random.random() * 0.1 * size.x * size.y)
            while len(blocks) < occupy:
                blocks.add(coord(random.randint(0, size.x - 1), random.randint(0, size.y - 1)))
 
        return cls(size, blocks)

    @classmethod
    def from_string(cls, world_desc: str) -> 'GridWorld':
        """
        Create a new grid world from a string describing the layout.

        Each line corresponds to a different row, and #s represent the position of a block, while any other character is interpreted as an empty square. The size of the world is the number of lines (height) and the size of the longest line (width). E.g.:

        ....#
        #....
        #....
        #....
        .....
        """
        BLOCK_STR = '#'
        rows = cleandoc(world_desc).splitlines()
        size = Coordinate(x=max(len(r) for r in rows), y=len(rows))
        return cls(size, blocks=cls.find_coordinates(BLOCK_STR, rows))

    @classmethod
    def from_dict(cls, desc: Dict[str, Any]):
        """
        Create a new grid world from a dictionary describing the layout.

        Keys:
            - map: contains a string or an array of strings with the the description of the map (see `from_string` method for details)
            - size: single or pair of integers specifying the size of the world (single for square). Mandatory if 'map' is missing.
            - block: list of pairs specifying the coordinates of blocks.
        """
        if 'map' in desc:
            map_str = desc['map'] if isinstance(desc['map'], str) else "\n".join(str(line) for line in desc['map'])
            world = cls.from_string(map_str)
        else:
            if 'size' not in desc:
                raise GridWorldException('Missing world size!')
            size = Coordinate(x=desc['size'], y=desc['size']) if isinstance(desc['size'], int) else Coordinate(x=desc['size'][0], y=desc['size'][1])
            world = cls(size, [])
        for pos in desc.get('block', []):
            world.addBlock(Coordinate(x=pos[0], y=pos[1]))
        return world

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert a world into its dictionary description.
        """
        desc_dict = {}

        size = self.size
        blocks = list(self.blocks)

        if len(blocks) < (0.1 * size.x * size.y):
            desc_dict['size'] = tuple((size.x, size.y))
            if len(blocks) > 0:
                desc_dict['block'] = [tuple((pos.x, pos.y)) for pos in blocks]
        else:
            map_rows = []
            for y in range(size.y - 1, -1, -1):
                row = ''.join('#' if self.isBlock(coord(x, y)) else '.' for x in range(0, size.x))
                map_rows.append(row)
            desc_dict['map'] = '\n'.join(map_rows)

        return desc_dict

    @classmethod
    def from_JSON(cls, json_desc):
        """
        Create a new grid world from a JSON string or document object describing the layout. See method `from_dict` for details on the required keys and their values. For backward compatibility it accepts also a dictionary, which is passed directly to `from_dict` method.
        """
        if isinstance(json_desc, collections.abc.Mapping):
            dict_desc = json_desc
        elif isinstance(json_desc, str):
            dict_desc = json.loads(json_desc)
        else:
            dict_desc = json.load(json_desc)
        return cls.from_dict(dict_desc)

    def to_JSON(self, fp):
        """
        Serialize a world as a JSON formatted stream to fp (a .write()-supporting file-like object, see json.dump for details).
        """
        json.dump(self.to_dict(), fp)

    def to_JSONs(self) -> str:
        """
        Return a serialization of the world as a JSON formatted string.
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def find_coordinates(items: str, world_desc: Union[str, Iterable[str]]):
        """Return all the coordinates in which any of the characters appears in the world description. The description can be a multiline string or the list of lines."""
        coordinates = []
        rows = world_desc.splitlines() if isinstance(world_desc, str) else world_desc
        y = -1
        for row in reversed(rows):
            y += 1
            for x in range(len(row)):
                if row[x] in items:
                    coordinates.append(Coordinate(x=x, y=y))
        return coordinates

    @property
    def size(self) -> Coordinate:
        """Return the size of the world."""
        return self._size

    @property
    def blocks(self) -> Set[Coordinate]:
        """Return the set of coordinates where blocks are placed."""
        return self._blocks

    @property
    def object_locations(self) -> Dict[WorldObject, Coordinate]:
        """Return a dictionary associating objects to their coordinate."""
        return self._objects

    @property
    def location_objects(self) -> Dict[Coordinate, Iterable[WorldObject]]:
        """Return a dictionary associating locations to the objects at the given coordinate."""
        return self._location

    def isBlock(self, pos: Coordinate) -> bool:
        """Return true if in the coordinate there's a block."""
        return pos in self.blocks

    def isInside(self, pos: Coordinate) -> bool:
        """Return true if the coordinate is inside the world."""
        return (0 <= pos.x < self.size.x) and (0 <= pos.y < self.size.y)

    def objects_at(self, pos: Coordinate) -> Iterable[WorldObject]:
        """Return an iterable over the objects at the given coordinate."""
        return self.location_objects.get(pos, [])

    def location_of(self, obj: WorldObject) -> Coordinate:
        """Return the coordinate of the object within the world, or none if it's not in it."""
        return self.object_locations.get(obj, None)

    def empty_cells(self, count_objects=False) -> Iterable[Coordinate]:
        """Return an iterable object over the cells without blocks. If count_objects is not False then also other objects are taken into account."""
        all_cells = set([coord(x, y) for x in range(0, self.size.x) for y in range(0, self.size.y)])
        all_cells.difference_update(self.blocks)
        if count_objects:
            all_cells.difference_update(self.location_objects.keys())
        return all_cells

    @property
    def objects(self) -> Iterable[WorldObject]:
        """Return an iterable over the objects within the world."""
        return self.object_locations.keys()

    def removeBlock(self, pos: Coordinate):
        self._blocks.discard(pos)

    def addBlock(self, pos: Coordinate):
        self._blocks.add(pos)

    def addObject(self, obj: WorldObject, pos: Coordinate):
        if not self.isInside(pos):
            raise OutOfBounds('Placing {} outside the world at {}'.format(obj, pos))
        if self.isBlock(pos):
            raise Collision('Placing {} inside a block {}'.format(obj, pos))
        if pos in self.location_objects:
            self.location_objects[pos].append(obj)
        else:
            self.location_objects[pos] = [obj]
        self.object_locations[obj] = pos
        obj._setWorld(self)

    def removeObject(self, obj: WorldObject):
        try:
            self.location_objects[self.location_of(obj)].remove(obj)
            del self.object_locations[obj]
            obj._setWorld(None)
        except KeyError:
            pass
        except ValueError:
            pass

    def moveObject(self, obj: WorldObject, pos: Coordinate):
        if not self.isInside(pos):
            raise OutOfBounds('Moving {} outside the world at {}'.format(obj, pos))
        if self.isBlock(pos):
            raise Collision('Moving {} inside a block {}'.format(obj, pos))
        old_pos = self.object_locations.get(obj, None)
        if old_pos in self.location_objects:
            self.location_objects[old_pos].remove(obj)
        if pos in self.location_objects:
            self.location_objects[pos].append(obj)
        else:
            self.location_objects[pos] = [obj]
        self.object_locations[obj] = pos
        obj._setWorld(self)

    def __str__(self):
        CELL_WIDTH = 1
        BLANK = '.'.rjust(CELL_WIDTH)
        BLOCK = '██' * CELL_WIDTH
        maze_strs = [[BLANK for j in range(self.size.x)] for i in range(self.size.y)]

        for pos in self.blocks:
            maze_strs[pos.y][pos.x] = BLOCK

        for obj, pos in self.object_locations.items():
            maze_strs[pos.y][pos.x] = obj.charSymbol().ljust(CELL_WIDTH)

        top_frame = '┌' + '──' * CELL_WIDTH * self.size.x + '┐' + '\n'
        bottom_frame = '\n' + '└' + '──' * CELL_WIDTH * self.size.x + '┘'
        side_frame = '│'

        return ascii_to_wide(top_frame + "\n".join(reversed([side_frame + ''.join(maze_strs[i]) + side_frame for i in range(self.size.y)])) + bottom_frame)


#######################################
#   Simple agent moving in four directions that eats on the way.
#   Its goal is to consume all the food


class Food(WorldObject):
    """Food in the EaterWorld, it can be consumed by the Eater agent."""
    def charSymbol(self):
        return '🍌'


class Eater(Agent):
    """An agent that moves in the EaterWorld. It can move in 4 directions (Eater.Actions) and consumes Food objects that are in the cells where it moves. It sees its position and smells whether there's still food in the world (Eater.Percept). Its goal is to consume all the food in the environment."""
    class Actions(Actions):
        """Eater actions for each direction in which the agent can move (N, S, E, W)"""
        N = (0, 1)
        S = (0, -1)
        E = (1, 0)
        W = (-1, 0)

    @dataclass(frozen=True)
    class Percept(Percept):
        """Eater agent perception: the current position and whether there's more food."""
        position: Coordinate
        more_food: bool

    def __init__(self):
        self._foodcount = 0
        self._reward = 0
        self.FOOD_BONUS = 10
        self._alive = True

    def charSymbol(self):
        return '🐒'

    @property
    def isAlive(self):
        """Return true is the agent can still execute actions."""
        return self._alive

    @property
    def reward(self) -> int:
        """The current accumulated reward"""
        return self._reward

    def do(self, action: Agent.Actions) -> int:
        delta = action.value
        new_pos = coord(self.location.x + delta[0], self.location.y + delta[1])
        try:
            self.world.moveObject(self, new_pos)
        except (OutOfBounds, Collision):
            pass
        # every action costs 1
        cost = -1
        for obj in self.world.objects_at(self.location):
            if isinstance(obj, Food):
                # eat the food
                self.world.removeObject(obj)
                self._foodcount += 1
                # food give bonus!
                cost += self.FOOD_BONUS
        self._reward += cost
        return cost

    def suicide(self) -> int:
        """Kill the agent, returns the outcome of the action."""
        self._alive = False
        # no penalty for suicide
        return 0

    def percept(self) -> 'Eater.Percept':
        return self.Percept(
            position=self.location,
            more_food=any(isinstance(o, Food) for o in self.world.objects)
        )

    def success(self) -> bool:
        """Return true once all the food has been consumed."""
        food = [o for o in self.world.objects if isinstance(o, Food)]
        return len(food) == 0


class EaterWorld(GridWorld):
    """A GridWorld which contains Food and a Eater agent that can move within the world and eat the food when it moves in a cell that contains some food.
    """
    @classmethod
    def random(cls, map_desc: str=None, size: Coordinate=None, blocks: Iterable[Coordinate]=[], food_amount: float=.1, **kwargs) -> 'EaterWorld':
        """Create a new world from the map description and randomly place food until the given percentage of the free space is filled. If the food amount is greater or equal than 1 then it's interpreted as the number of food objects to include.

        Args:
            map_desc (str, optional): map of the world. Defaults to None.
            size (Coordinate, optional): size of the world. Defaults to None.
            blocks (Iterable[Coordinate], optional): location of the blocks. Defaults to [].
            food_amount (float, optional): the amount of food to add. Default 10% of the available cells.


        Raises:
            GridWorldException: if the world cannot be created

        Returns:
            EaterWorld: a new random world
        """

        world = super().random(map_desc=map_desc, size=size, blocks=blocks, **kwargs)

        free_cells = list(world.empty_cells())
        random.shuffle(free_cells)
        if len(free_cells) < 1:
            raise GridWorldException('No space for placing food and agent in the world')

        world.addObject(Eater(), free_cells.pop())

        food_count = int(food_amount) if food_amount >= 1 else int(len(free_cells) * food_amount)
        for i in range(food_count):
            world.addObject(Food(), free_cells.pop())

        return world

    @classmethod
    def from_dict(cls, desc: Dict[str, Any]):
        """
        Create a new grid world from a dictionary describing the layout.

        Keys (include keys of `GridWorld`):
            - eater: agent position (random if missing)
            - food:  list of food positions
        """
        world = super().from_dict(desc)

        for pos in [coord(*loc) for loc in desc.get('food', [])]:
            if not world.isBlock(pos):
                world.addObject(Food(), pos)

        if 'eater' in desc:
            world.add_eater(coord(*desc['eater']))
        else:
            world.add_eater()

        return world

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert a world into its dictionary description.
        """
        desc_dict = super().to_dict()
        desc_dict['food'] = []

        for o in self.objects:
            if isinstance(o, Eater):
                desc_dict['eater'] = (o.location.x, o.location.y)
            elif isinstance(o, Food):
                desc_dict['food'].append(tuple((o.location.x, o.location.y)))

        return desc_dict

    def add_eater(self, location: Coordinate = None):
        """
        Add an Eater agent at the given coordinates or a random place if the location is not provided.

        Raise exceptions if the agent cannot be placed in the given position or there's no space.
        """
        agent = Eater()
        if location is not None:
            self.addObject(agent, location)
        else:
            free_cells = list(self.empty_cells(count_objects=True))
            random.shuffle(free_cells)
            if len(free_cells) < 1:
                raise GridWorldException('No space for placing the agent in the world')
            self.addObject(agent, free_cells.pop())


MAP_STR = """
    ################
    #    #    #    #
    #         #    #
    #    #         #
    #    #    #    #
    ############# ##
    #    #    #    #
    #    #    #    #
    #    #    #    #
    #              #
    ############# ##
    #    #    #    #
    #         #    #
    #    #         #
    #    #    #    #
    ################
    """
