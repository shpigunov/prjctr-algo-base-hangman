"""
Adversary strategies.

Each strategy takes a `Game` object as a parameter in order to have access 
to the game's word list and other parameters.
"""

import random
import game


def adv0(game):
    """Random adversary - choose random word from word list"""
    return random.choice(game.word_list)