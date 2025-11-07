# Lab 02: Offline search and Wumpus

During this lab we are going to apply the search framework to a variation of the previous GridWorld problem which is a modified version of [Hunt the Wumpus](https://en.wikipedia.org/wiki/Hunt_the_Wumpus).

This assignment **will be marked** and contribute to the final marking of the course.


## Offline search for the Wumpus

The description of Hunt the Wumpus game is available in a [separate page](markdown/hunt-the-wumpus.md). To test your algorithm we will be using a simulator, based on the same GridWorld code used during the last week.


## Setup the coding environment

For this lab, you can use the virtual environment `iap` which contains all the packages that we will use throughout the entire course.

If the environment is set up on your machine,  activate it (e.g., `conda activate iap2223`).

- For this assignment you should work on the `offline-wumpus` folder.

# Structure of the code

The WumpusWorld is implemented in the same package `wumpus` used for the previous assignment, so it shares the same API. The difference lies in the structure of the world, objects it may contain, and the capability of the agent (the [wumpus.Hunter](https://gitlab.inf.unibz.it/Davide.Lanti1/wumpus-tessaris/-/blob/master/wumpus/wumpus.py#L39)] class).

The actions of the agent, so those that your player should return, can be accessed via the [wumpus.Hunter.Actions](https://gitlab.inf.unibz.it/Davide.Lanti1/wumpus-tessaris/-/blob/master/wumpus/wumpus.py#L41) class and correspond to the one described in the game:

~~~
$ pydoc wumpus.Hunter.Actions
Help on class Actions in wumpus.Hunter:

wumpus.Hunter.Actions = class Actions(wumpus.gridworld.Actions)
 |  An enumeration.
 |  
 |  Method resolution order:
 |      Actions
 |      wumpus.gridworld.Actions
 |      enum.Enum
 |      builtins.object
 |  
 |  Data and other attributes defined here:
 |  
 |  CLIMB = <Actions.CLIMB: 5>
 |  GRAB = <Actions.GRAB: 4>
 |  LEFT = <Actions.LEFT: 2>
 |  MOVE = <Actions.MOVE: 0>
 |  RIGHT = <Actions.RIGHT: 1>
 |  SHOOT = <Actions.SHOOT: 3>
~~~

The [examples](https://gitlab.inf.unibz.it/Davide.Lanti1/wumpus-tessaris/-/tree/master/examples) directory contains an example of usage of the WumpusWorld in the file `examples/wumpus_usage.py`, which can be used to play different versions of the game. For testing your code you could also specify the layout of the world using a JSON file: an example of such a file can be found in `resources/wumpus-world.json`.

# Tasks

As in the previous assignment, your task is to implement a player that perform an offline search for a sequence of moves to solve the game and then simply execute them when asked via the play method.

Your code must be runnable via the `gridrunner` script which takes as input the reference to the class implementing the player. By default the script adds the current directory to the Python search path (`sys.path`) but an alternative path could be added with the `--path` option. For example the player in `examples/wumpus_usage.py` could be run using:

~~~
gridrunner --world WumpusWorld --entry wumpus_usage:GooPlayer
~~~

# Implement the search for the Wumpus

Your task is to create a player (a subclass of `wumpus.OfflinePlayer`) able to control the hunter in such a way that it maximise its outcome. The size and layout of the world will be randomly generated but your player will have access to the world and agent instances (see `GooPlayer` in `examples/wumpus_usage.py` for details on how to use them). You can make the following assumptions, following the classic game setup:

- the environment is a square
- there is exactly a wumpus
- there is exactly a gold ingot
- the environment doesn't contain any block
- the hunter is always starting in the bottom left corner facing upward (north)
- there is a single exit placed in the same square where the hunter starts

Note that it's **not guaranteed** that the gold ingot is always reachable; that is there might be cases in which the gold ingot is not reachable and the strategy to maximise the outcome is to climb out immediately.

Offline search is a much simpler setting w.r.t. the original game. To have an idea on how difficult it'll be for the online case, where only perception are available, you can try to play it with:

~~~
python wumpus_usage.py real_deal
~~~

## Evaluate your code

Compare the different search techniques in terms of:

- number of visited nodes, and
- the quality of solution (i.e. the outcome of the game).

# Submission

Write a `SOLUTION.md` file in the `wumpus-offline` directory describing your code and how to use it (the format is a lightweight markup language called Markdown which gets nicely rendered by the GitLab file viewer), then create an annotated tag and push it to the GitLab server.

You should thoroughly describe your code and the results of your evaluation. If you prefer to keep a small `SOLUTION.md` file, you can also include a separate documentation file using the format you prefer.

**This lab will be part of the evaluation!**
