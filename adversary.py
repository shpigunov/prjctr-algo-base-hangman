"""
Adversary strategies.

Each strategy takes a `Game` object as a parameter in order to have access 
to the game's word list and other parameters.
"""

import numpy as np
import random

import game
import functions


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
        

def adv2(game, play_results='play3.csv', selection=10):
    
    # Build scorecard from csv
    f = open('play3.csv', 'r')
    scorecard = {}
    for line in f.readlines():
        word, difficulty = line.split(',')
        scorecard[word.lower()] = int(difficulty)
    f.close()
    
    # Calculate letter 'difficulty' from scorecard
    d = functions.calculate_letter_difficulty(scorecard)
    
    # Make a selection of specified size
    selection = [random.choice(game.word_list) for i in range(0, selection)]
    
    # Pick most difficult word from selection
    word = ''
    difficulty = 0
    for w in selection:
        word_diff = functions.assess_word_difficulty(w, d)
        if word_diff > difficulty:
            difficulty = word_diff
            word = w

    return word