# Online search and Wumpus

During this lab we are going to apply the search framework to a variation of the previous GridWorld problem which is a modified version of [Hunt the Wumpus](https://en.wikipedia.org/wiki/Hunt_the_Wumpus).
The description of the Hunt the Wumpus game is available in a [separate page](markdown/hunt-the-wumpus.md). To test your algorithm we will be using a simulator, based on the same GridWorld code used in other labs.

**This assignment will be marked** and contribute to the final marking of the course.

### Setup the coding environment

For this lab, you can use the virtual environment `iap` which contains all the packages that we will use throughout the entire course. Remind that the command to activate the environment is the following:

~~~
    conda activate iap
~~~

If you won't use Anaconda you can create a virtual environment by hand or using any other virtual environment manager (see [The Hitchhiker's Guide to Python!](https://docs.python-guide.org/dev/virtualenvs/) for details), taking the list of required packages from [environment.yaml](https://ole.unibz.it/mod/page/view.php?id=171313).

To check whether the environment is working you can use the following command to play a random version of the game:

~~~
gridrunner --world WumpusWorld --entry wumpus:UserPlayer
~~~

## Wumpus API

As in the previous _offline wumpus_ you should implement a player subclass; in this case `wumpus.OnlinePlayer`:

~~~
$ pydoc wumpus.OnlinePlayer
wumpus.OnlinePlayer = class OnlinePlayer(builtins.object)
 |  wumpus.OnlinePlayer(name: str = None)
 |  
 |  A player for a given agent. It implements the play method which should
 |  return one of the actions for the agent or None to give up.
 |  
 |  Methods defined here:
 |  
 |  end_episode(self, outcome: int, alive: bool, success: bool)
 |      Method called at the when an episode is completed with the outcome of the game and whether the agent was still alive and successfull.
 |  
 |  play(self, percept: wumpus.gridworld.Percept, actions: Iterable[wumpus.gridworld.Agent.Actions], reward: Union[int, NoneType]) -> wumpus.gridworld.Agent.Actions
 |      Given a percept, which might differ according to the specific problem, and the list of valid actions, returns an action to play at the given turn or None to stop the episode. The reward is the one obtained in the previous action, on the first turn its value is None.
 |  
 |  start_episode(self)
 |      Method called at the beginning of the episode.
~~~

Contrary to `wumpus.OfflinePlayer` your player doesn't receive a description of the initial world with the `start_episode` method, and at each turn the `play` method is called to ask for the move to perform. To see an example of a general implementation (not specific to the `WumpusWorld`) you can look at the code for [wumpus.UserPlayer](https://gitlab.inf.unibz.it/Davide.Lanti1/wumpus-tessaris/-/blob/master/wumpus/player.py#L78). The method should return an action and is called with 3 parameters:

- `percept`: the current perception of the world, an instance of the class `wumpus.Hunter.Percept` with the boolean attributes `stench`, `breeze`, `bump`, `scream`, `glitter`. Their semantics is described in the [Hunt the Wumpus](markdown/hunt_the_wumpus.md) document, whereas the implementation is in [wumpus.Hunter.Percept](https://gitlab.inf.unibz.it/Davide.Lanti1/wumpus-tessaris/-/blob/master/wumpus/wumpus.py#L56).
- `actions`: the set of available actions (same as `wumpus.OfflinePlayer`).
- `reward`: the reward of the previous action, the first time the method is called with a `None` value.

## Tasks

Your task is to create a player (a subclass of `wumpus.OnlinePlayer`) able to control the hunter in such a way that it maximizes its outcome. The size and layout of the world will be randomly generated but you can make **the following assumptions**, following the classic game setup:

- the environment is a square
- there is exactly one wumpus
- there is exactly one gold ingot
- the environment doesn't contain any block
- the hunter is always starting in the bottom left corner facing upward (north)
- there is a single exit placed in the same square where the hunter starts

Note that it's **not guaranteed** that the gold ingot is always reachable; that is, there might be cases in which the gold ingot is not reachable, in which case the strategy to maximize the outcome is to climb out immediately.

Your code must be runnable via the `gridrunner` script which takes as input the reference to the class implementing the player. By default the script adds the current directory to the Python search path ([sys.path](https://docs.python.org/3/library/sys.html#sys.path)) but an alternative path could be added with the `--path` option. For example the player `wumpus.UserPlayer` could be run using:

~~~
gridrunner --world WumpusWorld --entry wumpus.UserPlayer
~~~

## Evaluate your code

You should evaluate your player by considering the average score on randomly generated worlds.

## Submission

Write a `SOLUTION.md` file describing your code and how to use it (the format is a lightweight markup language called [Markdown](https://gitlab.inf.unibz.it/help/user/markdown.md) which gets nicely rendered by the GitLab file viewer), then push your solution to the GitLab server.

You should thoroughly describe your code and the results of your evaluation. If you prefer to keep a small `SOLUTION.md` file, you can also include a separate documentation file using the format you prefer.

Again, **this lab will be part of the evaluation!**
