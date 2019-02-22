"""
Adversary strategies.

Each strategy takes a `Game` object as a parameter in order to have access 
to the game's word list and other parameters.
"""

import numpy as np

import random
import game


def adv0(game):
    """Random adversary - choose random word from word list"""
    return random.choice(game.word_list)

def adv1(game, play_results='play3.csv', threshold=0):
    """Adversary strategy using words from known results of a 
    player strategy.
    
    The basic idea is that this player uses a pre-generated list
    of results of a play-through by a certain player that looks like:
    
    `jazz, 21
    fizz, 20
    buzz, 15
    anaconda, 0`
    
    etc., and uses the number of attempts as weights in a discrete 
    distibution function. In practice this means that words more 
    difficult to a player will be selected more often.
    """
    
    f = open(play_results, 'r')
    
    words = []
    probabilities = []
    
    for line in f.readlines():
        # Read & parse file
        word, difficulty = line.split(',')
        difficulty = int(difficulty)
        
        # Cut off all words guessed with 0 wrong attempts
        # becuase they won't be selected anyway
        if difficulty > threshold:
            words.append(word)
            probabilities.append(difficulty)
    
    # Normalize probabilities so that they sum up to 1
    s = sum(probabilities)
    probabilities = [p / s for p in probabilities]
    
    f.close()

    return np.random.choice(words, 1, p=probabilities)[0]
        
        
    