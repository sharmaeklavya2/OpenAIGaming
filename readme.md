# OpenAI Gaming

Play games in the OpenAI gym using the keyboard.

Example invocation: `python3 play.py CartPole-v1 --delay=50`

## Mapping format

For this to work, the computer must know a mapping from keyboard keys to actions.
Mappings can be specified as JSON files.
To create a mapping for a game with id `x`, create the JSON file `keymaps/x.json`.

Keys of the mapping can be:

* `"default"`
* any alphanumeric character
* the name of any `pynput.keyboard.Key` object, like `"left"`, `"right"`, `"space"`

Values of the mapping can be:

* a number
* an array of floats (if actions are multi-dimensional)
* the values `"next"`, `"prev"`, `"random"`.

Apart from this, for discrete-action games, unmapped keys from 0 to 9 are mapped to corresponding actions of the same number.
This can be a good way to explore actions in a game and devise an appropriate keymap for it.

## List all games

To list the games supported by the OpenAI gym, run this:

```python
import gym.envs
for game_name in gym.envs.registry.env_specs.keys():
    print(game_name)
```
