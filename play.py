#!/usr/bin/env python3

"""
Play OpenAI gym's games using the keyboard.
"""

import sys
import os
import time
import math
import random
import logging
import argparse
import json

import gym
from gym import wrappers
from pynput.keyboard import Key, Listener


class InputState(object):
    def __init__(self, action_space, keymap):
        self.pressed_keys = set()
        self.pressed_key = None
        self.recent_action = None
        self.user_stop = False
        self.keymap = keymap
        self.action_space = action_space


def get_action(input_state):
    key = input_state.pressed_key
    key2 = None
    if key is not None:
        if isinstance(key, Key):
            key2 = key.name
        else:
            try:
                key2 = key.char
            except AttributeError:
                logging.warning('Invalid key {}'.format(repr(repr(key))))

    keymap = input_state.keymap
    default_action = keymap['default']
    action = default_action
    action_space = input_state.action_space
    if key2 is not None:
        if key2 in keymap:
            action = keymap[key2]
        elif key2.isdigit():
            n = int(key2)
            if isinstance(action_space, gym.spaces.Discrete) and n < action_space.n:
                action = n

    if action == 'same':
        action = input_state.recent_action
    elif action == 'next' or action == 'prev':
        delta = 1 if action == 'next' else -1
        if isinstance(action_space, gym.spaces.Discrete):
            if input_state.recent_action is None:
                action = 0
            else:
                action = (input_state.recent_action + delta) % action_space.n
        else:
            logging.warning("'next' does not make sense for continuous action space")
            action = action_space.sample()
    elif action == 'random' or action == 'rand':
        action = action_space.sample()
    input_state.recent_action = action
    return action


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', help='Name of the game')
    parser.add_argument('--force-continue', action='store_true', default=False,
        help="Keep playing even after 'Game over'")
    parser.add_argument('--delay', type=float, help='Extra delay between frames in milliseconds')
#   parser.add_argument('-o', '--output', help='Path to file in which gameplay will be stored')
    args = parser.parse_args()

    # Get keymap
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    keymap_fpath_prefix = os.path.join(BASE_DIR, 'keymaps', args.game)
    keymap_fpath_json = keymap_fpath_prefix + '.json'
    try:
        with open(keymap_fpath_json) as fobj:
            print('Using JSON keymap', file=sys.stderr)
            keymap = {key.lower(): value for key, value in json.load(fobj).items()}
    except FileNotFoundError:
        logging.warning('No keymap found')
        keymap = {}
    if 'default' not in keymap:
        keymap['default'] = 'random'

    # Initialization
    env = gym.make(args.game)
    state = env.reset()
    done = False
    t = 0
    score = 0
    input_state = InputState(env.action_space, keymap)
    print('Action space:', env.action_space)

    def keypress_callback(key):
        input_state.pressed_key = key
        input_state.pressed_keys.add(key)

    def keyrelease_callback(key):
        input_state.pressed_keys.remove(key)
        if input_state.pressed_keys:
            input_state.pressed_key = next(iter(input_state.pressed_keys))
        else:
            input_state.pressed_key = None
        # Check for Ctrl+C
        try:
            if key.char == 'c' and input_state.pressed_keys in ({Key.ctrl}, {Key.ctrl_r}):
                print('Ctrl+C')
                input_state.user_stop = True
        except AttributeError:
            pass

    with Listener(on_press=keypress_callback, on_release=keyrelease_callback) as listener:
        try:
            while not input_state.user_stop and (args.force_continue or not done):
                env.render()
                action = get_action(input_state)
                state2, reward, done, info = env.step(action)
                if args.delay is not None:
                    time.sleep(args.delay / 1000)
                t += 1
                score += reward
                state = state2
        except KeyboardInterrupt:
            pass
        print('Time:', t)
        print('Score:', score)
        env.close()


if __name__ == '__main__':
    main()
