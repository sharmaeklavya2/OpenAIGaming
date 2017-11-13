# OpenAI Gaming

Play games in the [OpenAI gym](https://gym.openai.com/envs/) using the keyboard.

Example invocation: `python3 play.py CartPole-v1 --delay=50`

It is also possible to record a game (using the `-o` command-line switch).
This can be used for apprenticeship learning.

## Mapping format

For every game, the computer must know a mapping from keyboard keys to actions.
Mappings can be specified as JSON files.
To create a mapping for a game with id `x`, create the JSON file `keymaps/x.json`.

Keys of the mapping can be:

* `"default"`
* any alphanumeric character
* the name of any `pynput.keyboard.Key` object, like `"left"`, `"right"`, `"space"`

Values of the mapping can be:

* a number
* an array of floats (if actions are multi-dimensional)
* `"next"` or `"prev"`: If actions are discrete, they are numbered from `0` to `n-1`.
  If the action performed in the previous instant was `x`, `"next"` will perform the action `(x+1)%n`
  and `"prev"` will perform the action `(x-1)%n`.
* `"same"`: Perform the same action which was performed in the last instant.
* `"random"`: Randomly sample an action from the action space.

When no valid key is pressed, the action performed is the one corresponding to `"default"`.
If `"default"` action is not specified, it is taken as `"random"`.

For discrete-action games, unmapped keys from 0 to 9 are mapped to corresponding actions of the same number.
This can be a good way to explore actions in a game and devise an appropriate keymap for it.

## Recording a game

A game will be recorded in several files.
If the environment is queried `t` times using `env.step`, then:

* `states.npy` contains the `t+1` states seen in the game.
* `actions.npy` contains the `t` actions selected by the player.
* `rewards.npy` contains the `t` rewards obtained by the player.
* `metadata.json` contains shapes and data types of states, actions and rewards
  and miscellaneous data like total playing time, total score, whether game was interrupted, etc.

All these files will be created in a directory whose path is specified in the `-o` command-line switch.

## List all games

To list the games supported by the OpenAI gym, run this:

```python
import gym.envs
for game_name in gym.envs.registry.env_specs.keys():
    print(game_name)
```
